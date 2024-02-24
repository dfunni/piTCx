from src.devices import MCP9800
import smbus2 as smbus

i2c_bus = smbus.SMBus(bus=1)
dev = MCP9800(i2c_bus)


def test_init():
    assert dev.address is 0x48
    assert dev.res is 0b11 << 5
    assert dev.config is 0b01111001

def test_one_shot_converstion():
    dev.one_shot_conversion()
    assert dev.config is 0b11111001
    
def test_set_oneshot():
    dev.set_oneshot(1)
    assert dev.config is 0b11111001
    dev.set_oneshot(0)
    assert dev.config is 0b01111001

def test_set_resolution():
    dev.set_resolution(9)
    assert dev.config is 0b00011001
    assert dev.res is 0b00 << 5
    assert dev.convert_time == 0.03
    dev.set_resolution(10)
    assert dev.config is 0b00111001
    assert dev.res is 0b01 << 5
    assert dev.convert_time == 0.06
    dev.set_resolution(11)
    assert dev.config is 0b01011001
    assert dev.res is 0b10 << 5
    assert dev.convert_time == 0.12
    dev.set_resolution(12)
    assert dev.config is 0b01111001
    assert dev.res is 0b11 << 5
    assert dev.convert_time == 0.24

def test_set_alert():
    dev.set_alert(0, 0, 0)
    assert dev.alert is 0b00000
    dev.set_alert(1, 1, 1)
    assert dev.alert is 0b01110
    dev.set_alert(3, 0, 0)
    assert dev.config is 0b01111001

def test_set_shutdown():
    dev.set_shutdown(0)
    assert dev.shutdown is 0b0
    dev.set_shutdown(1)
    assert dev.shutdown is 0b1

def test_read_register():
    config = dev.read_register(1)[0]
    assert config is 0b01111001
    config = dev.read_register(3)
    assert len(config) is 2

def test_read():
    temp = dev.read()
    assert temp > 0

def test_one_shot_read():
    temp = dev.one_shot_read()
    assert temp > 0
    dev.no_io = True
    assert dev.one_shot_read() == 20.0
    dev.no_io = False
