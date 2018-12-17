import microbit
import ustruct
from micropython import const

_GIGGLEBOT_ADDRESS      = const(0x04)

_GET_FIRMWARE_VERSION   = b'\x01'
_GET_MANUFACTURER       = b'\x02'
_GET_BOARD              = b'\x03'
_GET_VOLTAGE_BATTERY    = b'\x04'
_GET_LINE_SENSORS       = b'\x05'
_GET_LIGHT_SENSORS      = b'\x06'
_GET_MOTOR_STATUS_RIGHT = b'\x07'
_GET_MOTOR_STATUS_LEFT  = b'\x08'
_SET_MOTOR_POWER        = b'\x09'
_SET_MOTOR_POWERS       = b'\x0a'
_GET_VOLTAGE_RAIL       = b'\x0b'

MOTOR_RIGHT             = b'\x01'
MOTOR_LEFT              = b'\x02'

_MOTOR_FLOAT            = const(-128)

class GiggleBot():

    def __init__(self):
        self.write = microbit.i2c.write
        self.read = microbit.i2c.read
        self.buff = bytearray(8)

    def get_manufacturer(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_MANUFACTURER)
        return str(self.read(_GIGGLEBOT_ADDRESS, 20), 'utf-8').strip()
        
    def get_board(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_BOARD)
        return str(self.read(_GIGGLEBOT_ADDRESS, 20), 'utf-8').strip()

    def get_version_firmware(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_FIRMWARE_VERSION)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0]
        
    def get_voltage_battery(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_VOLTAGE_BATTERY)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0] / 1000

    def get_voltage_rail(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_VOLTAGE_RAIL)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0] / 1000

    def get_line_sensors(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_LINE_SENSORS)
        array = self.read(_GIGGLEBOT_ADDRESS, 3)

        for i in b'\x00\x01':
            ustruct.pack_into('f', self.buff, 1 - i, (1023 - (array[i] << 2) | (((array[2] << (i * 2)) & 0xC0) >> 6)) / 1023.0)
        
        return ustruct.unpack('ff', self.buff)
    
    def get_light_sensors(self):
        self.write(_GIGGLEBOT_ADDRESS, _GET_LIGHT_SENSORS)
        array = self.read(_GIGGLEBOT_ADDRESS, 3)

        for i in b'\x00\x01':
            ustruct.pack_into('f', self.buff, 1 - i, (1023 - (array[i] << 2) | (((array[2] << (i * 2)) & 0xC0) >> 6)) / 1023.0)
        
        return ustruct.unpack('ff', self.buff)
        
    def set_motor_power(self, port, power):
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWER + port + ustruct.pack('b', power))
        
    def set_motor_powers(self, powerLeft, powerRight):
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWERS + ustruct.pack('bb', powerRight, powerLeft))

    def get_motor_status(self, port):
        self.write(_GIGGLEBOT_ADDRESS, _GET_MOTOR_STATUS_LEFT if port == MOTOR_LEFT else _GET_MOTOR_STATUS_RIGHT)
        array = bytearray(self.read(_GIGGLEBOT_ADDRESS, 2))

        if array[1] & 0x80:
            array[1] -= 0x100

        return array

    def reset_all(self):
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWERS + ustruct.pack('bb', _MOTOR_FLOAT, _MOTOR_FLOAT))