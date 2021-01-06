import serial
import logging
import smbus2 as smbus
from devices.MCP3424 import MCP3424
from devices.MCP9800 import MCP9800
from devices import thermocouple as tc
from gpiozero import PWMOutputDevice
import time

logger = logging.getLogger(__name__)

class cmdHandler(object):

    def __init__(self, ser, i2c_id):
        self.ser = ser
        self.bus = smbus.SMBus(i2c_id)
        self.amb = MCP9800(self.bus)
        self.c0 = MCP3424(self.bus, chan=0, tc_type='k_type')
        self.c1 = MCP3424(self.bus, chan=1, tc_type='k_type')
        self.c2 = MCP3424(self.bus, chan=2, tc_type='k_type')
        self.c3 = MCP3424(self.bus, chan=3, tc_type='k_type')
        self.heater_duty = 0
        self.fan_duty = 0
        self.handler_dict = {'READ': self.handle_READ,
                             'CHAN': self.handle_CHAN,
                             'UNITS': self.handle_UNITS,
                             'OT1': self.handle_OT1,
                             'OT2': self.handle_OT2,
                             'IO3': self.handle_IO3,}
        self.dev_dict = {'amb': self.amb,
                         'tcs': []}
        self.units = "C"
        self.setting34 = False
        self.isinit = False # ensure CHAN before READ
        self.OT1 = PMWOutputDevice(4, frequency=100)

    def handle_command(self, cmd):
        cmd = cmd.decode('utf-8').replace('\n', '')
        self.cmd = str(cmd).split(';')
        action = self.handler_dict.get(self.cmd[0], self.handle_UNK)()

    def handle_READ(self):
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
        else:
            pass

    def handle_CHAN(self):
        self.isinit = True 
        self.chan_idx = [int(i)-1 for i in list(self.cmd[1])] # -1 if None
        set34 = -2 if self.chan_idx[2] == self.chan_idx[3] == -1 else None
        # truncate chan_idx and chans
        self.chan_idx = self.chan_idx[:set34] # truncating if no ArduionoTC4_34
        # Artisan is expecting either 2 or 4 temperatures
        chans = [self.c0, self.c1, self.c2, self.c3][:set34] + [None]
        self.dev_dict['tcs'] = [chans[i] for i in self.chan_idx] # reordering
        logger.info(len(chans))
        logger.info(f'Initialized: {self.cmd}, {self.chan_idx}')
        self.ser.write(b'#')
        self.handle_READ()

    def handle_UNITS(self):
        self.units = self.cmd[1]
        logger.info(f'Units: {self.units}')

    def handle_OT1(self):
        self.heater_duty = self.cmd[1]
        self.OT1.value = self.heater_duty / 100.0
        logger.info(f'OT1: {self.cmd}')

    def handle_OT2(self):
        self.fan_duty = self.cmd[1]
        logger.info(f'OT2: {self.cmd}')

    def handle_IO3(self):
        logger.info(f'IO3: {self.cmd}')

    def handle_UNK(self):
        logger.warning(f'Unknown command: {self.cmd}')


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    with serial.Serial('/dev/ttyS90') as ser:
        handler = cmdHandler(ser, 1)

        while(True):
            cmd = ser.readline()
            handler.handle_command(cmd)
                
