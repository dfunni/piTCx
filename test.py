import glob
import logging
import smbus2 as smbus
from devices.MCP342x import MCP342x
from devices.MCP3424 import MCP3424
from devices.MCP9800 import MCP9800

import numpy as np
from numpy.polynomial.polynomial import polyval
import time

logger = logging.getLogger(__name__)

def get_smbus():
    candidates = []
    prefix = '/dev/i2c-'
    for bus in glob.glob(prefix + '*'):
        try:
            n = int(bus.replace(prefix, ''))
            candidates.append(n)
        except:
            pass
        
    if len(candidates) == 1:
        return smbus.SMBus(candidates[0])
    elif len(candidates) == 0:
        raise Exception("Could not find an I2C bus")
    else:
        raise Exception("Multiple I2C busses found")

def mV_to_C(mV, temp_range='low'):

    coef_inv = {
        'neg': [0, 
                2.5173462e1,
                -1.1662878,
                -1.0833638,
                -8.9773540e-1,
                -3.7342377e-1,
                -8.6632643e-2,
                -1.0450598e-2,
                -5.1920577e-4],
        'low': [0,
                2.508355e1,
                7.860106e-2,
                -2.503131e-1,
                8.315270e-2,
                -1.228034e-2,
                9.804036e-4,
                -4.413030e-5,
                1.057734e-6,
                -1.052755e-8],
        'high': [-1.318058e2,
                4.830222e1,
                -1.646031,
                5.464731e-2,
                -9.650715e-4,
                8.802193e-6,
                -3.110810e-8],
                }

    return polyval(mV, coef_inv[temp_range])


def get_temp(tc, amb): 
    tc_mV = tc.convert_and_read() * 1000
    tc_C = mV_to_C(tc_mV, temp_range='low') # in 0-500C range
    amb_C = amb.read_temperature()
    return (tc_C + amb_C), amb_C


if __name__ == '__main__':

    logging.basicConfig(level='INFO')

    bus = get_smbus()

    amb = MCP9800(bus)
#    tc0 = MCP342x(bus, resolution=18, gain=8, channel=0)
    tc0 = MCP3424(bus)
    for i in range(10):
        temp_tc0, temp_amb = get_temp(tc0, amb)
        print(f'tc0: {temp_tc0}\tamb: {temp_amb}')
        time.sleep(1)

