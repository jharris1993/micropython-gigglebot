import microbit

class I2C:
    def __init__(self, address):
        """
        address - address of the device to communicate with
        """
        self.__write = microbit.i2c.write
        self.__read = microbit.i2c.read
        self.address = address

    def read(self, reg, no_bytes, repeat = False):
        """
        reg - the register to read from in bytes form object
        no_bytes - how many bits to read; a multiplier of 8
        repeat - specifies if a stop bit is sent
        returns - data in bytes format
        """
        self.__write(self.address, reg, repeat)
        return self.__read(self.address, no_bytes, repeat)

    def write(self, reg, args, repeat = False):
        """
        reg - register to write to; bytes object
        args - values to write to register; bytes object
        repeat - specifies if a stop bit is sent
        """
        self.__write(self.address, reg + args, repeat)