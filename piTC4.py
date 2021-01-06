import logging
import time
import smbus2 as smbus
from devices.MCP342x import MCP342x
from devices.MCP3424 import MCP3424
from devices.MCP9800 import MCP9800
from devices import thermocouple as tc

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logging.basicConfig(level='INFO')
    bus = smbus.SMBus(1) 
    amb = MCP9800(bus)
    tc0 = MCP3424(bus, chan=0, tc_type='k_type')
    tc1 = MCP3424(bus, chan=1, tc_type='k_type')
    #tc1 = MCP342x(bus, resolution=18, gain=8, channel=0)
    tcs = [tc0, tc1, None]
    tcs = [i for i in tcs if i]
    for i in range(5):
        t0 = time.time()

        dev_dict = {'amb': amb,
                    'tcs': tcs }
        T_Cs, T_Fs, dly  = tc.read_temps(dev_dict)
        temp_amb, temp_tc0, temp_tc1 = T_Cs
        t1 = time.time()
        print(f'{temp_amb},{temp_tc0},{temp_tc1}, dt:{t1-t0}')


