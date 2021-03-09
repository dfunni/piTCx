import sys
import serial
import logging
import time
import smbus2 as smbus

from gpiozero import PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

from devices import MCP342x, MCP9800
from devices import thermocouple as tc
import yaml

logger = logging.getLogger(__name__) 


class TCx(object):

    def __init__(self, ser, i2c_id, config='DEFAULT'):

        # ADC Setup
        self.ser = ser
        self.bus = smbus.SMBus(i2c_id)

        self.amb = MCP9800(self.bus)
        self.c0 = MCP342x(self.bus, chan=0, tc_type='k_type')
        self.c1 = MCP342x(self.bus, chan=1, tc_type='k_type')
        self.c2 = None
        self.c3 = None
        self.dev_dict = {'amb': self.amb,
                         'tcs': []}

        self.handler_dict = {'READ': self.handle_READ,
                             'CHAN': self.handle_CHAN,
                             'UNITS': self.handle_UNITS,
                             'OT1': self.handle_OT1,
                             'OT2': self.handle_OT2,
                             'IO2': self.handle_IO2,
                             'IO3': self.handle_IO3,
                             'FILT': self.handle_FILT,
                             'BUTTON':self.handle_BUTTON,}

        self.units = "C" # temperature units
        self.setting34 = False # TC channels 3/4 expected from Artisan
        self.isinit = False # ensure CHAN before READ

        # GPIO setup
        with open("/home/pi/TCx/config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader).get(config, 'DEFAULT')
        self.OT1pin = cfg['pOT1']
        self.OT2pin = cfg['pOT2']
        self.IO2pin = cfg['pIO2']

        self.heater_duty = 0
        self.fan_duty = 100
        self.dc_fan_duty = 0
        factory = PiGPIOFactory()
        self.OT1 = PWMOutputDevice(pin=self.OT1pin, pin_factory=factory)
        self.OT2 = PWMOutputDevice(pin=self.OT2pin, pin_factory=factory)
        self.IO2 = PWMOutputDevice(pin=self.IO2pin, pin_factory=factory)

        # variables for filter
        self.filt = [0] * 4
        self.prev_temps = [0] * 4

    def handle_command(self, cmd):
        '''Parses Artisan commands and takes appropriate action
        '''
        cmd = cmd.decode('utf-8').replace('\n', '')
        self.cmd = str(cmd).split(';')
        action = self.handler_dict.get(self.cmd[0], self.handle_UNK)()

    def handle_READ(self):
        '''Reads thermocouple temps and sends output over serial
        Command of type: READ
        '''
        if self.isinit:
            t0 = time.time()
            T_Cs, T_Fs, dly  = tc.read_temps(self.dev_dict)
            Ts = T_Fs if self.units == 'F' else T_Cs
            Ts = self.dofilter(Ts)
            AT = Ts[0]
            T_str = ','.join([f'{T}' for T in Ts[1:]])
            HT = self.heater_duty
            FN = self.fan_duty
            SV = 0
            temps = f'{AT},{T_str},{HT},{FN},{SV}'
            self.ser.write(bytes(temps, 'ascii'))
            logger.info(f'{time.time()}:{self.cmd}:{temps}')
        else: # if CHAN command has not been read yet
            pass

    def handle_FILT(self):
        '''Sets the filter values to a list of floats between 0 and 1
        Command of type: FILT;70;70;70;70
        '''
        filts = str(self.cmd[1]).split(',')
        self.filt = [int(i)/100.0 for i in filts]
        logger.info(f'{time.time()}:{self.cmd}:{self.filt}') 

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
        logger.info(f'{time.time()}:{self.cmd}:{self.chan_idx}')
        self.ser.write(b'#')
        self.handle_READ()

    def handle_UNITS(self):
        '''Sets temperature units.
        Command of type: UNITS;C
        '''
        self.units = self.cmd[1]
        logger.info(f'{time.time()}:{self.cmd}:{self.units}')

    def handle_OT1(self):
        '''Slow PWM eater control, 1 Hz
        COmmand of type: OT1;100
        '''
        self.heater_duty = self.cmd[1]
        duty = float(self.heater_duty) / 100.0
        if duty == 0:
            self.OT1.off()
        elif duty == 1:
            self.OT1.on()
        else:
            self.OT1.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info(f'{time.time()}:{self.cmd}:{self.heater_duty}')

    def handle_OT2(self):
        '''PWM AC fan cotrol, ZCD at IO2
        Command of type: OT2;100
        '''
        self.fan_duty = self.cmd[1]
        duty = float(self.fan_duty) / 100.0
        self.OT2.blink(on_time=duty, off_time=(1-duty), n=None)
        if duty == 0:
            self.OT2.off()
        elif duty == 1:
            self.OT2.on()
        else:
            self.OT2.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info(f'{time.time()}:{self.cmd}:{self.fan_duty}')

    def handle_IO2(self):
        '''For ZCD, TODO'''
        self.dc_fan_duty = self.cmd[1]
        duty = float(self.dc_fan_duty) / 100.0
        self.IO2.blink(on_time=duty, off_time=(1-duty), n=None)
        if duty == 0:
            self.IO2.off()
        elif duty == 1:
            self.IO2.on()
        else:
            self.IO2.blink(on_time=duty, off_time=(1-duty), n=None)
        logger.info(f'{time.time()}:{self.cmd}:{self.dc_fan_duty}')

    def handle_IO3(self):
        '''For DC fan control, TODO
        Command of type: IO3;100
        '''
        logger.info(f'{time.time()}:{self.cmd}')

    def handle_BUTTON(self):
        '''Log Artisan button presses
        Command of type: BUTTON;START
        '''
        logger.info(f'{time.time()}:{self.cmd}')
        
    def handle_UNK(self):
        '''All other commands'''
        logger.warning(f'{time.time()}:{self.cmd}:UNKNOWN')

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
    logging.basicConfig(filename='/home/pi/tcx.log', level='INFO')
    with serial.Serial('/dev/ttyS90') as ser:
        tc4 = TCx(ser, 1)

        while(True):
            try:
                cmd = ser.readline()
                tc4.handle_command(cmd)
            except KeyboardInterrupt:
                sys.exit()
                
                
