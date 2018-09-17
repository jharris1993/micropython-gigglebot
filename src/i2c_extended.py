# I2C functions
def __i2c_write_reg_8(addr, reg, val):
    microbit.i2c.write(addr, bytes([reg, val]), False)

def __i2c_write_reg_16(addr, reg, val):
    microbit.i2c.write(addr, bytes([reg, ((val >> 8) & 0xFF), (val & 0xFF)]), False)

def __i2c_write_reg_32(addr, reg, val):
    microbit.i2c.write(addr, bytes([reg, ((val >> 24) & 0xFF), ((val >> 16) & 0xFF), ((val >> 8) & 0xFF), (val & 0xFF)]), False)

def __i2c_write_reg_list(addr, reg, list):
    arr = [reg]
    arr.extend(list)
    microbit.i2c.write(addr, bytes(arr), False)

def __i2c_read_reg_8(addr, reg):
    microbit.i2c.write(addr, bytes([reg]), False)
    return microbit.i2c.read(addr, 1, False)[0]

def __i2c_read_reg_16(addr, reg):
    microbit.i2c.write(addr, bytes([reg]), False)
    buf = microbit.i2c.read(addr, 2, False)
    return ((buf[0] << 8) | buf[1])

def __i2c_read_reg_list(addr, reg, len):
    microbit.i2c.write(addr, bytes([reg]), False)
    return microbit.i2c.read(addr, len, False)