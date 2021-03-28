#!/usr/bin/env python3

# Microchip MCP9800 Temperature Sensor (I2C)
# By Michal Ludvig <mludvig@logix.net.nz>

import smbus2 as smbus
import logging
import time

__all__ = [ "MCP9800" ]

logger = logging.getLogger(__name__)

class MCP9800(object):

    REG_TEMP            = 0x00  # Temperature register
    REG_CONFIG          = 0x01  # Config register
    REG_HYSTERISIS      = 0x02  # Temperature Hysteresis register
    REG_LIMIT           = 0x03  # Temperature Limit-set register

    # Config register shifts, e.g. 12 bit resolution: CONFIG_VAL |= (0b11 << SHIFT_ADC_RES)
    SHIFT_ONE_SHOT      = 7     # One shot, 1=enabled, 0=disabled (default)
    SHIFT_ADC_RES       = 5     # ADC resolution (0b00 = 9bit , 0b01 = 10bit (0.25C), 0b10 = 11bit (0.125C), 0b11 = 12bit (0.0625C))
    SHIFT_FAULT_QUEUE   = 3     # Fault queue bits, 0b00 = 1 (default), 0b01 = 2, 0b10 = 4, 0b11 = 6
    SHIFT_ALERT_POLARITY= 2     # Alert polarity, 1= active high, 0 = active low (default)
    SHIFT_COMP_INTR     = 1     # 1 = Interrupt mode, 0 = Comparator mode (default)
    SHIFT_SHUTDOWN      = 0     # 1 = Enable shutdown, 0 = Disable shutdown (default)

    res_map = {9: 0b00,
               10: 0b01,
               11: 0b10,
               12: 0b11}

    ctime_map = {9: 30e-3,
                 10: 60e-3,
                 11: 120e-3,
                 12: 240e-3}

    def __init__(self, bus=None, i2c_id=1, address=0x48, res=12):

        if bus:
            self.bus = bus
        else:
            self.bus = smbus.SMBus(i2c_id)
        self.address = address
        self.tc_type = 'ref' 
        resb = self.res_map.get(res, 12)
        self.convert_time = self.ctime_map.get(res, 12)

        self.oneshot = 0b0 << self.SHIFT_ONE_SHOT # initial oneshot mode
        self.res = resb << self.SHIFT_ADC_RES
        self.alert = 0b1100 << self.SHIFT_COMP_INTR
        self.shutdown = 0b1 << self.SHIFT_SHUTDOWN
        self.no_io = False
        self.default_value = 20.0
        self.configure()

    def configure(self, source='init'):
        config = self.oneshot | self.res | self.alert | self.shutdown
        logger.debug(f'configuration: {source} {config:#010b}')
        try:
            self.bus.write_byte_data(self.address, self.REG_CONFIG, config)
        except:
            logger.warning('TCx hardware not connected, using default amb')
            self.no_io = True

    def convert(self):
        self.oneshot = 0b1 << self.SHIFT_ONE_SHOT # initial oneshot mode
        self.shutdown = 0b1 << self.SHIFT_SHUTDOWN
        self.configure('convert')
        pass

    def set_oneshot(self, enable):
        self.oneshot = enable << self.SHIFT_ONE_SHOT
        self.configure('mode')

    def set_resolution(self, bit_resolution):
        resb = self.res_map.get(bit_resolution, 12)
        self.convert_time = self.ctime_map.get(bit_resolution, 12)
        self.res = resb << self.SHIFT_ADC_RES
        self.configure('rsln')

    def set_alert(self, fault=3, alert_polarity=0, compint=0):
        alert = fault << self.SHIFT_FAULT_QUEUE
        alert |= alert_polarity << self.SHIFT_ALERT_POLARITY
        alert |= compint << self.SHIFT_COMP_INTR
        self.alert = alert
        self.configure('alrt')

    def set_shutdown(self, enable):
        self.shutdown = enable << self.SHIFT_SHUTDOWN
        self.configure('sdwn')

    def read_register(self, register, length):
        data = self.bus.read_i2c_block_data(self.address, register, length)
        return data

    def read(self):
        if self.no_io:
            return self.default_value
        temp = self.read_register(self.REG_TEMP, 2)
        if len(temp) < 2:
            logger.warning("bad read" + bin(temp))
            return  None
        return float((temp[0]<<8) + temp[1])/(2**8)

    def convert_and_read(self):
        self.convert()
        time.sleep(self.convert_time)
        return self.read()


if __name__ == "__main__":
    logging.basicConfig(level='DEBUG')
    mcp = MCP9800()
    #data = mcp.read_register(MCP9800.REG_CONFIG, 1)
    # print(f"CONF: {bin(data[0])}")
    print("Temperature: %.1f" % mcp.convert_and_read())

