import serial
import logging
import time
import smbus2 as smbus

from gpiozero import PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

from devices.MCP3424 import MCP3424
from devices.MCP9800 import MCP9800
from devices import thermocouple as tc

logger = logging.getLogger(__name__) 


class piTC4(object):

    def __init__(self, ser, i2c_id, config=None):

        self.ser = ser
        self.bus = smbus.SMBus(i2c_id)

        self.amb = MCP9800(self.bus)
        # ADC channels
        self.c0 = MCP3424(self.bus, chan=0, tc_type='k_type')
        self.c1 = MCP3424(self.bus, chan=1, tc_type='k_type')
        self.c2 = MCP3424(self.bus, chan=2, tc_type='k_type')
        self.c3 = MCP3424(self.bus, chan=3, tc_type='k_type')

        self.handler_dict = {'READ': self.handle_READ,
                             'CHAN': self.handle_CHAN,
                             'UNITS': self.handle_UNITS,
                             'OT1': self.handle_OT1,
                             'OT2': self.handle_OT2,
                             'IO3': self.handle_IO3,}

        self.dev_dict = {'amb': self.amb,
                         'tcs': []}

        self.units = "C" # temperature units
        self.setting34 = False # TC channels 3/4 expected from Artisan
        self.isinit = False # ensure CHAN before READ

        self.heater_duty = 0
        factory = PiGPIOFactory()
        self.OT1 = PWMOutputDevice(pin=18, pin_factory=factory)

        # Untested
        if config == 'CONFIG_PWM':
            # DC fan on IO3
            self.dc_fan_duty = 0
            self.IO3 = PWMOutputDevice(pin=23, pin_factory=factory)
        if config == "CONFIG_PAC":
            # AC fan on OT2, ZCD on IO2
            self.fan_duty = 0
            self.OT2 = PWMOutputDevice(pin=17, pin_factory=factory)
            self.IO2 = PWMOutputDevice(pin=22, pin_factory=factory)

    def handle_command(self, cmd):
        cmd = cmd.decode('utf-8').replace('\n', '')
        self.cmd = str(cmd).split(';')
        action = self.handler_dict.get(self.cmd[0], self.handle_UNK)()

    def handle_READ(self):
        '''Command of type: READ'''
        if self.isinit:
            t0 = time.time()
            T_Cs, T_Fs, dly  = tc.read_temps(self.dev_dict)
            Ts = T_Cs if self.units == 'F' else T_Cs
            AT = Ts[0]
            T_str = ','.join([f'{T}' for T in Ts[1:]])
            HT = self.heater_duty
            FN = self.fan_duty
            SV = 0
            temps = f'{AT},{T_str},{HT},{FN},{SV}'
            self.ser.write(bytes(temps, 'ascii'))
            logger.info(f'READ: temps - {temps} dt: {round(time.time()-t0,4)}')
        else: # if CHAN command has not been read yet
            pass

    def handle_CHAN(self):
        '''Initializes TC4, sets up channels for ET and BT
        Command of type: CHAN;1234
        '''
        self.isinit = True 
        self.chan_idx = [int(i)-1 for i in list(self.cmd[1])] # -1 if None
        set34 = -2 if self.chan_idx[2] == self.chan_idx[3] == -1 else None
        self.chan_idx = self.chan_idx[:set34] # truncating if no ArduionoTC4_34
        # Artisan is expecting either 2 or 4 temperatures
        chans = [self.c0, self.c1, self.c2, self.c3][:set34] + [None]
        self.dev_dict['tcs'] = [chans[i] for i in self.chan_idx] # reordering
        logger.info(len(chans))
        logger.info(f'Initialized: {self.cmd}, {self.chan_idx}')
        self.ser.write(b'#')
        self.handle_READ()

    def handle_UNITS(self):
        '''Sets temperature units.
        Command of type: UNITS;C
        '''
        self.units = self.cmd[1]
        logger.info(f'Units: {self.units}')

    def handle_OT1(self):
        '''Slow PWM eater control, 1 Hz
        COmmand of type: OT1;100
        '''
        self.heater_duty = self.cmd[1]
        duty = float(self.heater_duty) / 100.0
        self.OT1.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info(f'OT1: {self.heater_duty}')

    def handle_OT2(self):
        '''PWM AC fan cotrol, ZCD at IO2
        Command of type: OT2;100
        '''
        self.fan_duty = self.cmd[1]
        self.OT2.value = float(self.fan_duty) / 100.0
        logger.info(f'OT2: {self.fan_duty}')

    def handle_IO2(self):
        '''For ZCD, TODO'''
        logger.info(f'IO2: {self.cmd}')

    def handle_IO3(self):
        '''For DC fan control, TODO
        Command of type: OT2;100
        '''
        self.dc_fan_duty = self.cmd[1]
        self.IO3.value = float(self.dc_fan_duty) / 100.0
        logger.info(f'IO3: {self.dc_fan_duty}')

    def handle_UNK(self):
        '''All other commands'''
        logger.warning(f'Unknown command: {self.cmd}')


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    with serial.Serial('/dev/ttyS90') as ser:
        tc4 = piTC4(ser, 1)

        while(True):
            cmd = ser.readline()
            tc4.handle_command(cmd)
                
