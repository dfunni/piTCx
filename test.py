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
#    tc0 = MCP3424(bus)
    tc0 = MCP342x(bus, resolution=18, gain=8, channel=0)
#    tc1 = MCP342x(bus, resolution=18, gain=8, channel=1)
    for i in range(10):
        temp_tc0, temp_amb = tc.read_temp(tc0, amb)
#        temp_tc1, temp_amb = tc.read_temp(tc1, amb)
        temptc1 = 0
        temp_tc2 = 0
        temp_tc3 = 0
        heaterd = 100
        fand = 100
        sv = 0
        print(f'{temp_tc0},{temp_tc1},{temp_tc2},{temp_tc3},{heaterd},{fand},{sv},{temp_amb}')
        time.sleep(1)

