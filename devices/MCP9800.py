#!/usr/bin/env python3

# Microchip MCP9800 Temperature Sensor (I2C)
# By Michal Ludvig <mludvig@logix.net.nz>
import logging
import time
import smbus2 as smbus


__all__ = ["MCP9800"]

logger = logging.getLogger(__name__)


class MCP9800(object):
    """Class to represent the MPC9800 temperature sensor.

        CONFIG register:
                    x x x x x x x x
                    | [_] [_] | | |
        one-shot ___/  |   |  | | |
        resolution ____/   |  | | |
        fault queue _______/  | | |
        alert polarity _______/ | |
        COMP/INT _______________/ |
        shutdown _________________/

        One shot, 1=enabled, 0=disabled (default)
        ADC resolution: 0b00 = 9bit,
                        0b01 = 10bit (0.25C)
                        0b10 = 11bit (0.125C)
                        0b11 = 12bit (0.0625C)
        Fault queue bits, 0b00 = 1 (default), 0b01 = 2, 0b10 = 4, 0b11 = 6
        Alert polarity: 1 = active high, 0 = active low (default)
        Comparator/Interrupt: 1 = Interrupt mode, 0 = Comparator mode (default)
        Shutdown: 1 = Enable shutdown, 0 = Disable shutdown (default)
    """
    SHIFT_ONE_SHOT = 7
    SHIFT_ADC_RES = 5
    SHIFT_FAULT_QUEUE = 3
    SHIFT_ALERT_POLARITY = 2
    SHIFT_COMP_INTR = 1
    SHIFT_SHUTDOWN = 0

    REG_TEMP = 0x00  # address of Temperature register
    REG_CONFIG = 0x01  # address of Config register
    REG_HYSTERISIS = 0x02  # address of Temperature Hysteresis register
    REG_LIMIT = 0x03  # address of Temperature Limit-set register

    res_map = {9: 0b00,
               10: 0b01,
               11: 0b10,
               12: 0b11}

    ctime_map = {9: 30e-3,
                 10: 60e-3,
                 11: 120e-3,
                 12: 240e-3}

    def __init__(self, bus, address=0x48, res=12):

        self.bus = bus
        self.address = address
        self.tc_type = 'ref'
        resb = self.res_map.get(res, 12)
        self.convert_time = self.ctime_map.get(res, 12)

        self.oneshot = 0b0 << self.SHIFT_ONE_SHOT  # initialize 0 for 1shot
        self.res = resb << self.SHIFT_ADC_RES
        self.alert = 0b1100 << self.SHIFT_COMP_INTR  # falut+alert+comp/int
        self.shutdown = 0b1 << self.SHIFT_SHUTDOWN  # initialize 1 for 1shot
        self.no_io = False
        self.default_value = 20.0
        self.configure()

    def configure(self, source='init'):
        """Sets the sensor configuration register.
        """
        config = self.oneshot | self.res | self.alert | self.shutdown
        logger.debug('configuration: %s %s', source, format(config, '#010b'))
        try:
            self.bus.write_byte_data(self.address, self.REG_CONFIG, config)
        except IOError:
            logger.warning('TCx hardware not connected, using default amb')
            self.no_io = True

    def one_shot_conversion(self):
        """Run one-shot temperature reading.
        """
        self.oneshot = 0b1 << self.SHIFT_ONE_SHOT
        self.shutdown = 0b1 << self.SHIFT_SHUTDOWN
        self.configure('one_shot_conversion')

    def set_oneshot(self, enable):
        """Set the one shot bit of the sensor configuration register.
        """
        self.oneshot = enable << self.SHIFT_ONE_SHOT
        self.configure('mode')

    def set_resolution(self, bit_resolution):
        """Set resolution to 9, 10, 11, or 12 bits. Updates configuration
        register and conversion time.
        """
        resb = self.res_map.get(bit_resolution, 12)
        self.convert_time = self.ctime_map.get(bit_resolution, 12)
        self.res = resb << self.SHIFT_ADC_RES
        self.configure('rsln')

    def set_alert(self, fault=3, alert_polarity=0, compint=0):
        """Sets the fault queue, alert polarity, and
        comparator/inturrupt bits of the sensor configuration register.
        """
        alert = fault << self.SHIFT_FAULT_QUEUE
        alert |= alert_polarity << self.SHIFT_ALERT_POLARITY
        alert |= compint << self.SHIFT_COMP_INTR
        self.alert = alert
        self.configure('alrt')

    def set_shutdown(self, enable):
        """Set the shutdown bit of the sensor configuration register.
        """
        self.shutdown = enable << self.SHIFT_SHUTDOWN
        self.configure('sdwn')

    def read_register(self, register):
        """Reads a register specified by the register argument.
            Register addresses:
                0: ambient temperature register
                1: sensor configuration register
                2: temperature hysteresis register
                3: temperature limit-set register

        Args:
            register (int): address of the register to read in range 0..3
        """
        assert register in [0, 1, 2, 3], 'invalid register specified'
        if register == 1:
            length = 1  # config register is 1 byte
        else:
            length = 2  # all other registers are 2 bytes
        return self.bus.read_i2c_block_data(self.address, register, length)

    def read(self):
        """Read the temperature register and returns the value as a float.
        """
        if self.no_io:
            return self.default_value
        temp = self.read_register(self.REG_TEMP)
        if len(temp) < 2:
            logger.warning("bad read %s", bin(temp))
            return None
        return float((temp[0] << 8) + temp[1])/(2**8)

    def one_shot_read(self):
        """Read a one-shot temperature conversion.
        """
        self.one_shot_conversion()
        time.sleep(self.convert_time)
        return self.read()


if __name__ == "__main__":
    logging.basicConfig(level='DEBUG')
    i2c_bus = smbus.SMBus(bus=1)
    mcp = MCP9800(i2c_bus)
    data = mcp.read_register(MCP9800.REG_CONFIG)
    print(f"config: {bin(data[0])}")
    print("Temperature: %.1f", mcp.one_shot_read())
