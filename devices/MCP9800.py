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

    def __init__(self, bus=None, i2c_id=1, address=0x48, resolution=12):
        """
        MCP9800(bus = None, i2c_id = 0, address = 0x48)

        Either call with pre-initialised smbus(-compatible) instance in 'bus'
        Or with /dev/i2c-<id> device id in 'i2c_id' to open a new bus instance

        Usual MCP980x-family addresses are 0x48 ~ 0x4D
        """
        self.address = address
        if bus:
            self.bus = bus
        else:
            self.bus = smbus.SMBus(i2c_id)

        self.oneshot = 0b1 << self.SHIFT_ONE_SHOT
        self.res = 0b11 << self.SHIFT_ADC_RES
        self.alert = 0b1100 << self.SHIFT_COMP_INTR
        self.shutdown = 0b1 << self.SHIFT_SHUTDOWN
        self.configure()

    def set_oneshot(self, enable):
        self.oneshot = enable << self.SHIFT_ONE_SHOT
        self.configure()

    def set_resolution(self, bit_resolution):
        assert(bit_resolution >= 9 and bit_resolution <= 12)
        self.res = (int(bit_resolution) - 9) << self.SHIFT_ADC_RES
        self.configure()

    def set_alert(self, fault=3, alert_polarity=0, compint=0):
        alert = fault << self.SHIFT_FAULT_QUEUE
        alert |= alert_polarity << self.SHIFT_ALERT_POLARITY
        alert |= compint << self.SHIFT_COMP_INTR
        self.alert = alert
        self.configure()

    def set_shutdown(self, enable):
        self.shutdown = enable << self.SHIFT_SHUTDOWN
        self.configure()

    def configure(self):
        config = self.oneshot | self.res | self.alert | self.shutdown
        logger.debug(f'configuration: {bin(config)}')
        self.bus.write_byte_data(self.address, self.REG_CONFIG, config)

    def read_register(self, register, length):
        data = self.bus.read_i2c_block_data(self.address, register, length)
        return data

    def read_temperature(self):
        temp = self.read_register(self.REG_TEMP, 2)
        if len(temp) < 2:
            return None
        return float((temp[0]<<8) + temp[1])/(2**8)


if __name__ == "__main__":
    logging.basicConfig(level='DEBUG')
    mcp = MCP9800(i2c_id=1, address=0x48)
    mcp.set_oneshot(0)
    mcp.set_resolution(9)
    mcp.set_alert(0, 0, 0)
    mcp.set_shutdown(0)
    mcp.set_shutdown(1)
    mcp.set_oneshot(1)
    mcp.set_resolution(12)
    mcp.set_alert(3, 1, 1)
    #data = mcp.read_register(MCP9800.REG_CONFIG, 1)
    # print(f"CONF: {bin(data[0])}")
    print("Temperature: %.1f" % mcp.read_temperature())

