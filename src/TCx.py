import logging
import sys
import serial
import yaml
from argparse import ArgumentParser

import smbus2 as smbus

from gpiozero import PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

from devices import MCP342x, MCP9800
from devices import thermocouple as tc

logger = logging.getLogger(__name__)


class TCx(object):
    """This is a class for the TCx Raspberry Pi HAT.
    """

    def __init__(self, serial_bus, config):
        """Initializes the TCx instance based on serial bus used.

        Args:
            serial_bus (serial.Serial): Defines the main communication bus.

        """

        # ADC Setup
        self.serial_bus = serial_bus
        self.i2c_bus = smbus.SMBus(bus=1)  # I2C bus 1 is always used with GPIO

        self.amb = MCP9800(bus=self.i2c_bus)
        self.c0 = MCP342x(bus=self.i2c_bus, chan=0, tc_type='k_type')
        self.c1 = MCP342x(bus=self.i2c_bus, chan=1, tc_type='k_type')
        self.c2 = MCP342x(bus=self.i2c_bus, chan=2, tc_type='k_type')
        self.c3 = MCP342x(bus=self.i2c_bus, chan=3, tc_type='k_type')
        self.device_dict = {'amb': self.amb,
                            'tcs': []}

        self.handler_dict = {'READ': self.handle_read,
                             'CHAN': self.handle_chan,
                             'UNITS': self.handle_units,
                             'OT1': self.handle_ot1,
                             'OT2': self.handle_ot2,
                             'IO2': self.handle_io2,
                             'IO3': self.handle_io3,
                             'FILT': self.handle_filt,
                             'BUTTON': self.handle_button,
                             }

        self.units = "C"  # temperature units
        self.isinit = False  # ensure CHAN before READ

        # GPIO setup
        pins = config['PIN_CONFIG']
        factory = PiGPIOFactory()
        self.ot1 = PWMOutputDevice(pin=pins['pOT1'], pin_factory=factory)
        self.ot2 = PWMOutputDevice(pin=pins['pOT2'], pin_factory=factory)
        self.io2 = PWMOutputDevice(pin=pins['pIO2'], pin_factory=factory)

        self.heater_duty = 0
        self.fan_duty = 100  # assumption that fan is on to start
        self.dc_fan_duty = 0

        # variables for filter
        self.filt = [0] * 4
        self.prev_temps = [0] * 4
        self.cmd = None  # initialize
        self.chan_idx = []  # initialize

    def decode_command(self, cmd):
        '''Parses Artisan commands and takes appropriate action
        '''
        cmd = cmd.decode('utf-8').replace('\n', '')
        self.cmd = str(cmd).split(';')
        _ = self.handler_dict.get(self.cmd[0], self.handle_unknown)()

    def handle_read(self):
        '''Reads thermocouple temps and sends output over serial
        Command of type: READ
        '''
        if self.isinit:
            T_Cs, T_Fs, _ = tc.read_temps(self.device_dict)
            Ts = T_Fs if self.units == 'F' else T_Cs
            Ts = self.dofilter(Ts)
            AT = Ts[0]
            if len(Ts[1:]) == 1:
                Ts.append(0.0)
            T_str = ','.join([f'{T}' for T in Ts[1:]])
            HT = self.heater_duty
            FN = self.fan_duty
            SV = 0
            msg = f'{AT},{T_str},{HT},{FN},{SV}'
            self.serial_bus.write(bytes(msg, 'ascii'))
            logger.info('%s:%s', self.cmd, msg)
        else:  # if CHAN command has not been read yet
            logger.warning("READ before CHAN command")

    def handle_filt(self):
        '''Sets the filter values to a list of floats between 0 and 1
        Command of type: FILT;70;70;70;70
        '''
        filts = str(self.cmd[1]).split(',')
        self.filt = [int(i)/100.0 for i in filts]
        logger.info('%s:%s', self.cmd, self.filt)

    def handle_chan(self):
        '''Initializes TC4, sets up channels for ET and BT
        Command of type: CHAN;1234

        - A 0 index means there is no channel assigned to that value.
        - If Arduino_34 is not set the last two values will be 0 and we should
        omit them from chans.
        - Channel values from the command are reduced by one to index the
        proper ADC channel.
        Examples:
        CHAN;0100 results from ET: None, BT: ADC channel 0, Arduino_34 off
        CHAN;2134 results from ET: ADC channel 1, BT channel 2, Arduino_34 on
        '''
        self.isinit = True
        self.chan_idx = [int(i)-1 for i in list(self.cmd[1])]  # -1 if None
        # truncate unused channels if artisan setup with no ArduinoTC4_34
        if self.cmd[1][-2:] == '00':
            self.chan_idx = self.chan_idx[:-2]
        # None is included in chans to be indexed by a -1, ie no tc selected
        chans = [self.c0, self.c1, self.c2, self.c3, None]
        logger.info(self.chan_idx)
        self.device_dict['tcs'] = [chans[i] for i in self.chan_idx]
        logger.info(self.device_dict['tcs'])
        logger.info('%s:%s', self.cmd, self.chan_idx)
        self.serial_bus.write(b'#')
        self.handle_read()

    def handle_units(self):
        '''Sets temperature units.
        Command of type: UNITS;C
        '''
        self.units = self.cmd[1]
        logger.info('%s:%s', self.cmd, self.units)

    def handle_ot1(self):
        '''Slow PWM eater control, 1 Hz
        COmmand of type: OT1;100
        '''
        self.heater_duty = self.cmd[1]
        duty = float(self.heater_duty) / 100.0
        if duty == 0:
            self.ot1.off()
        elif duty == 1:
            self.ot1.on()
        else:
            self.ot1.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info('%s:%s', self.cmd, self.heater_duty)

    def handle_ot2(self):
        '''PWM AC fan cotrol, ZCD at IO2
        Command of type: OT2;100
        '''
        self.fan_duty = self.cmd[1]
        duty = float(self.fan_duty) / 100.0
        self.ot2.blink(on_time=duty, off_time=(1-duty), n=None)
        if duty == 0:
            self.ot2.off()
        elif duty == 1:
            self.ot2.on()
        else:
            self.ot2.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info('%s:%s', self.cmd, self.fan_duty)

    def handle_io2(self):
        '''For ZCD, TODO'''
        self.dc_fan_duty = self.cmd[1]
        duty = float(self.dc_fan_duty) / 100.0
        self.io2.blink(on_time=duty, off_time=(1-duty), n=None)
        if duty == 0:
            self.io2.off()
        elif duty == 1:
            self.io2.on()
        else:
            self.io2.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info('%s:%s', self.cmd, self.dc_fan_duty)

    def handle_io3(self):
        '''For DC fan control, TODO
        Command of type: IO3;100
        '''
        logger.info(self.cmd)

    def handle_button(self):
        '''Log Artisan button presses
        Command of type: BUTTON;START
        '''
        logger.info(self.cmd)

    def handle_unknown(self):
        '''All other commands'''
        logger.warning('%s is not implemented yet', self.cmd)

    def dofilter(self, temps):
        '''Simple IIR filter over all temperatures read:
                y[k] = y[k-1]*f - x[k]*(1-f)
        where f is the filter value between 0 and 1
        '''
        tmp = [self.prev_temps[i]*self.filt[i] for i, temp in enumerate(temps)]
        y = [tmp[i] + temp*(1-self.filt[i]) for i, temp in enumerate(temps)]
        self.prev_temps = y
        return y


if __name__ == '__main__':
    parser = ArgumentParser(description="Handles interfaces for TCx hardware.")
    ArgumentParser()
    parser.add_argument('user', metavar='USER', type=str,
                        help='the user where TCx code is located')
    args = parser.parse_args()
    with open(f"/home/{args.user}/TCx/config.yml", 'r',
              encoding="utf-8") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    logging.basicConfig(filename=config['LOG_FILE'],
                        format=config['LOG_FORMAT'],
                        datefmt=config['LOG_DATEFMT'],
                        level=config['LOG_LEVEL'])
    with serial.Serial('/dev/ttyS90') as ser:
        tc4 = TCx(ser, config)

        while True:
            try:
                command = ser.readline()
                tc4.decode_command(command)
            except KeyboardInterrupt:
                sys.exit()
