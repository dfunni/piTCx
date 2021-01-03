import logging
import smbus2 as smbus

logger = logging.getLogger(__name__)

class MCP3424(object):
    """
    Class to represent MCP3424 ADC.
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

    def __init__(self, bus=None, i2c_id=1, address=0x68):
        if bus:
            self.bus = bus
        else:
            self.bus = smbus.SMBus(i2c_id)
        self.address = address
        self.nrdy = 0b0 << self.SHIFT_NRDY
        self.chan = 0b00 << self.SHIFT_CHAN
        self.mode = 0b0 << self.SHIFT_MODE
        self.rsln = 0b11 << self.SHIFT_RSLN
        self.gain = 0b11 << self.SHIFT_GAIN
        self.configure('init')
        self.lsb = self.lsb_map.get(18)
        self.nbytes = self.nbytes_map.get(18)

    def __repr__(self):
        addr = hex(self.address)
        return (type(self).__name__ + ': device=' + self.device 
                + ', address=' + addr)

    def configure(self, source):
        self.config = self.nrdy | self.chan | self.mode | self.rsln | self.gain
        logger.debug(f'configuring {self.address}: {source} {self.config:#010b}')
        self.bus.write_byte(self.address, self.config)

    def convert(self):
        # No effect in continuous mode, initiates conversion in oneshot mode
        self.config |= 0x10000000
        self.configure('convert')
        self.config &= ~0x10000000

    def set_chan(self, chan):
        self.chan = chan << self.SHIFT_CHAN
        self.configure('chan')

    def set_mode(self, mode):
        self.mode = self.mode_map.get(mode, 'oneshot') << self.SHIFT_MODE
        self.configure('mode')
 
    def set_rsln(self, rsln):
        self.rsln = self.rsln_map.get(rsln, 18) << self.SHIFT_RSLN
        self.lsb = self.lsb_map.get(rsln, 18)
        self.nbytes = nbytes_map(rsln, 18)
        self.configure('rsln')

    def set_gain(self, gain):
        self.gain = self.gain_map.get(gain, 8) << self.SHIFT_GAIN
        self.configure('gain')

    def raw_read(self):
        res = self.rsln 
        while True:
            d = self.bus.read_i2c_block_data(self.address, 
                                             self.config, 
                                             self.nbytes)
            config_used = d[-1]
            if config_used & 0b10000000 == 0:
                count = 0
                for i in range(self.nbytes - 1):
                    count <<= 8
                    count |= d[i]
                sign_bit_mask = 1 << (self.rsln - 1)
                count_mask = sign_bit_mask - 1
                sign_bit = count & sign_bit_mask
                count &= count_mask
                if sign_bit:
                    count = -(~count & count_mask) - 1
                
                return count, config_used
                    
    def read(self, raw=False):
        count, config_used = self.raw_read()
        if config_used != self.config:
            raise Exception(f'Config does not match {config_used:#010b} != {self.config:#010b}')
        
        if raw:
            return count
        voltage = count * self.lsb / self.gain
        return voltage

    def convert_and_read(self, 
                         samples=None,
                         aggregate=None,
                         **kwargs):
        if samples is not None:
            r = [0] * samples
        for sn in ([0] if samples is None else range(samples)):
            self.convert()
            val = self.read(**kwargs)
            if samples is not None:
                r[sn] = val
            else:
                r = val
        if aggregate:
            r = aggregate(r)
        return r


if __name__ == '__main__':
    import time
    logging.basicConfig(level='DEBUG')
    tc0 = MCP3424()
    for i in range(5):
        print(tc0.convert_and_read() * 1000)
        time.sleep(1)
