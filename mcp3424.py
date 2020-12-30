import smbus2 as smbus

DEVICE_BUS = 1
ADC_ADDR = 0x68
AMB_ADDR = 0x48
    
def request_from(addr, nbytes):
    with smbus.SMBus(DEVICE_BUS) as bus:
        data = [bus.read_byte(addr) for i in range(nbytes)]
    return data

def read_uV():
    data = request_from(ADC_ADDR, 4)
    v = (data[0] << 16) | (data[1] << 8) | data[2]
    stat = data[3]
    #v *= 1000
    return v

if __name__ == '__main__':
    data = read_uV()
    print(bin(data), hex(data))
