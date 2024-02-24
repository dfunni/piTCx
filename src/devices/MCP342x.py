import logging
import time
import smbus2 as smbus

logger = logging.getLogger(__name__)


class MCP342x(object):
    """Class to represent MCP342x ADC.

        configuration register:
                    x x x x x x x x
                    | [_] | [_] [_]
        not ready __/  |  |  |   |
        channel _______/  |  |   |
        mode _____________/  |   |
        resolution __________/   |
        gain ____________________/

        not ready: 1=output not updated, 0=output reg has updated value
        channel: 00 = channel 1 (default)
                 01 = channel 2
                 10 = channel 3 MCP3424 only, treated as “00” by MCP3422/3
                 11 = channel 4 MCP3424 only, treated as “01” by MCP3422/3
        mode: 1=continuous converstion (default), 0=one-shot mode
        resolution: 00 = 12bit / 240 SPS (default)
                    01 = 14bit / 60 SPS
                    10 = 16bit / 15 SPS
                    11 = 18bit / 3.75 SPS
        gain: 00=x1 (default)
              01=x2
              10=x4
              11=x8
    """
    SHIFT_NRDY = 7
    SHIFT_CHAN = 5
    SHIFT_MODE = 4
    SHIFT_RSLN = 2
    SHIFT_GAIN = 0

    mode_map = {'continuous': 0b1,
                'oneshot': 0b0}

    rsln_map = {12: 0b00,
                14: 0b01,
                16: 0b10,
                18: 0b11}

    gain_map = {1: 0b00,
                2: 0b01,
                4: 0b10,
                8: 0b11}

    lsb_map = {12: 1e-3,
               14: 250e-6,
               16: 62.5e-6,
               18: 15.625e-6}

    nbytes_map = {12: 3,
                  14: 3,
                  16: 3,
                  18: 4}

    convert_map = {12: 1.0/240,
                   14: 1.0/60,
                   16: 1.0/15,
                   18: 1.0/3.75}

    def __init__(self,
                 bus,
                 address=0x68,
                 tc_type=None,
                 chan=0b00,
                 pga=8,
                 res=16):

        self.bus = bus
        self.address = address
        self.tc_type = tc_type
        self.res = res
        self.nrdy = 0b0 << self.SHIFT_NRDY
        self.chan = chan << self.SHIFT_CHAN
        self.mode = 0b0 << self.SHIFT_MODE  # initialize to one-shot
        self.rsln = self.rsln_map.get(res, 18) << self.SHIFT_RSLN
        self.gain = self.gain_map.get(pga, 8) << self.SHIFT_GAIN

        self.no_io = False
        self.configure('init')

        self.pga = pga
        self.lsb = self.lsb_map.get(res, 18)
        self.nbytes = self.nbytes_map.get(res, 18)
        self.convert_time = self.convert_map.get(res, 18)

    def __repr__(self):
        """Representation of the class showing the address and channel
        """
        addr = hex(self.address)
        chan = self.chan >> self.SHIFT_CHAN
        return f'{type(self).__name__}: address={addr}, chan={chan}'

    def configure(self, src):
        """Set the configuration register.
        """
        self.config = self.nrdy | self.chan | self.mode | self.rsln | self.gain
        logger.debug('configuring %s: %s %s',
                     hex(self.address), src, format(self.config, '#010b'))
        try:
            self.bus.write_byte(self.address, self.config)
            logger.debug('%s-%s', src, format(self.config, '#010b'))
        except IOError:
            logger.warning("I2C bus issue, setting temps to 0")
            self.no_io = True

    def convert(self):
        """Run one-shot temperature reading.
        """
        # No effect in continuous mode, initiates conversion in oneshot mode
        nrdy = 0b1 << self.SHIFT_NRDY
        config = nrdy | self.chan | self.mode | self.rsln | self.gain
        logger.debug('configuring %s: convert %s',
                     hex(self.address), format(config, '#010b'))
        self.bus.write_byte(self.address, config)

    def set_chan(self, chan):
        """Set the channel in the config register.
        """
        assert chan in [0, 1, 2, 3], 'invalid channel specified'
        self.chan = chan << self.SHIFT_CHAN
        self.configure('chan')

    def set_mode(self, mode):
        """Set the mode in the config register.
        """
        self.mode = self.mode_map.get(mode, 'oneshot') << self.SHIFT_MODE
        self.configure('mode')

    def set_rsln(self, rsln):
        """Set the resolution in the config register
        """
        self.rsln = self.rsln_map.get(rsln, 18) << self.SHIFT_RSLN
        self.lsb = self.lsb_map.get(rsln, 18)
        self.nbytes = self.nbytes_map.get(rsln, 18)
        self.convert_time = self.convert_map.get(rsln, 18)
        self.res = rsln
        self.configure('rsln')

    def set_gain(self, pga):
        """Set the gain in the config regitster
        """
        self.pga = pga
        self.gain = self.gain_map.get(pga, 8) << self.SHIFT_GAIN
        self.configure('gain')

    def raw_read(self):
        """Monitor bus until conversion is done, then read raw.
        """
        while True:
            d = self.bus.read_i2c_block_data(self.address,
                                             self.config,
                                             self.nbytes)
            config_used = d[-1]
            if (config_used & 0b10000000) == 0:  # conversion complete
                count = 0
                for i in range(self.nbytes - 1):  # read data not config
                    count <<= 8
                    count |= d[i]
                sign_bit_mask = 1 << (self.res - 1)
                count_mask = sign_bit_mask - 1
                sign_bit = count & sign_bit_mask
                count &= count_mask
                if sign_bit:
                    count = -(~count & count_mask) - 1
                logger.debug('count: %s, sign_bit: %s',
                             bin(count), bin(sign_bit))
                return count, config_used

    def read(self, raw=False):
        """Convert the raw count to a voltage reading.
        """
        count, config_used = self.raw_read()
        if config_used != self.config:
            c1 = bin(config_used)
            c2 = bin(self.config)
            logging.error('configuration error: %s != %s', c1, c2)
            return -1
        if raw:
            return count
        voltage = count * self.lsb / self.pga
        return voltage

    def convert_and_read(self, samples=None, **kwargs):
        """Runs one-shot conversion and reads values.
        """
        if self.no_io:
            return ([.01] if samples is None else [.01]*samples)
        if samples is not None:
            r = [0] * samples
        for sn in ([0] if samples is None else range(samples)):
            self.convert()
            time.sleep(0.95 * self.convert_time)
            val = self.read(**kwargs)
            if samples is not None:
                r[sn] = val
            else:
                r = val
        return r


# if __name__ == '__main__':
#     logging.basicConfig(level='DEBUG')
#     i2c_bus = smbus.SMBus(bus=1)
#     tc0 = MCP342x(i2c_bus)
#     for _ in range(5):
#         v = tc0.convert_and_read()
#         print(v)
#         time.sleep(1)
