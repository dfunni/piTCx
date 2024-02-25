from src.devices import MCP342x
from src.devices import TC
import smbus2 as smbus


i2c_bus = smbus.SMBus(bus=1)
dev = TC(bus=i2c_bus, chan=0b0)


def test_init():
    assert dev.address is 0x68
    assert dev.tc_type is 'k_type'
    assert dev.temp_range is 'low'

def test_volt_to_celcius():
    temp = dev.voltage_to_celcius(0.001)
    assert temp == 24.9836
    temp = dev.voltage_to_celcius(0.0)
    assert temp == 0.0
    temp = dev.voltage_to_celcius(0.020664)
    assert temp == 500.4479
