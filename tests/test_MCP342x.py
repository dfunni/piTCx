from src.devices import MCP342x
import smbus2 as smbus
import time

i2c_bus = smbus.SMBus(bus=1)
dev = MCP342x(i2c_bus)


def test_init():
    assert dev.address is 0x68
    assert dev.rsln is 0b10 << 2
    assert dev.config is 0b00001011

def test__repr__():
    assert dev.__repr__() == 'MCP342x: address=0x68, chan=0'

def test_raw_read():
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_set_chan():
    """Only using channels 0 and 1 for compatability with MCP3422
    """
    dev.set_chan(1)
    _, config = dev.raw_read()
    assert config is 0b00101011
    dev.set_chan(0)
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_set_mode():
    dev.set_mode('oneshot')
    _, config = dev.raw_read()
    assert config is 0b00001011
    dev.set_mode('continuous')
    _, config = dev.raw_read()
    assert config is 0b00011011
    dev.set_mode('oneshot') # reset to default

def test_set_rsln():
    dev.set_rsln(12)
    _, config = dev.raw_read()
    assert config is 0b00000011
    dev.set_rsln(14)
    _, config = dev.raw_read()
    assert config is 0b00000111
    dev.set_rsln(18)
    _, config = dev.raw_read()
    assert config is 0b00001111
    dev.set_rsln(16)
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_set_gain():
    dev.set_gain(1)
    _, config = dev.raw_read()
    assert config is 0b00001000
    dev.set_gain(2)
    _, config = dev.raw_read()
    assert config is 0b00001001
    dev.set_gain(4)
    _, config = dev.raw_read()
    assert config is 0b00001010
    dev.set_gain(8)
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_convert():
    dev.convert()
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_convert_and_read():
    r = dev.convert_and_read()
    assert r != 0
    dev.no_io = True
    r = dev.convert_and_read()
    assert r == [0.01]
    r = dev.convert_and_read(samples=3)
    assert r == [0.01, 0.01, 0.01]
    dev.no_io = False
    r = dev.convert_and_read(samples=1)
    assert len(r) is 1
    _, config = dev.raw_read()
    assert config is 0b00001011

def test_read():
    val = dev.read(raw=True)
    assert type(val) is int
    val = dev.read(raw=False)
    assert type(val) is not int
    assert val != 0
    dev.config = 0b10001011
    val = dev.read()
    assert val == -1