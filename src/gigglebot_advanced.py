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
_GET_MOTOR_STATUS_LEFT  = b'\x07'
_GET_MOTOR_STATUS_RIGHT = b'\x08'
_SET_MOTOR_POWER        = b'\x09'
_SET_MOTOR_POWERS       = b'\x0a'
_GET_VOLTAGE_RAIL       = b'\x0b'

MOTOR_RIGHT             = b'\x01' #: Left motor constant.
MOTOR_LEFT              = b'\x02' #: Right motor constant.

_MOTOR_FLOAT            = const(-128)

class GiggleBot():
    '''
    Slightly more advanced class to interface with the `GiggleBot`_ hardware.
    '''

    def __init__(self):
        '''
        Constructor to initialize a :py:class:`~gigglebot_advanced.GiggleBot` object.
        '''
        self.write = microbit.i2c.write
        self.read = microbit.i2c.read
        self.buff = bytearray(8)

    def get_manufacturer(self):
        '''
        Gets the manufacturer name.

        :returns: The manufacturer name of the board.
        :rtype: string

        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_MANUFACTURER)
        return str(self.read(_GIGGLEBOT_ADDRESS, 20), 'utf-8').strip()
        
    def get_board(self):
        '''
        Gets the name of the board.

        :returns: The name of the board.
        :rtype: string
        
        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_BOARD)
        return str(self.read(_GIGGLEBOT_ADDRESS, 20), 'utf-8').strip()

    def get_version_firmware(self):
        '''
        Gets the firmware version of the GiggleBot board (not the micro:bit's).

        :returns: Firmware version of the GiggleBot board.
        :rtype: int
        
        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_FIRMWARE_VERSION)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0]
        
    def get_voltage_battery(self):
        '''
        Gets voltage of the battery. 
        
        If the power switch is off, the value returned is unequivocally close to **0**.

        :returns: The battery voltage.
        :rtype: float
        
        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_VOLTAGE_BATTERY)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0] / 1000

    def get_voltage_rail(self):
        '''
        Gets the rail voltage.

        :returns: Rail voltage.
        :rtype: float

        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_VOLTAGE_RAIL)
        return ustruct.unpack('>H', self.read(_GIGGLEBOT_ADDRESS, 2))[0] / 1000

    def get_line_sensors(self):
        '''
        The line sensor values on the GiggleBot.

        Lower values indicate a darker material and on the opposite, higher values signify lighter colors (closing to white).

        :returns: A 2-element tuple with the values of the left and right sensor in this specific order.
        :rtype: tuple(int,int)
        
        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_LINE_SENSORS)
        array = self.read(_GIGGLEBOT_ADDRESS, 3)

        for i in b'\x00\x01':
            ustruct.pack_into('f', self.buff, 1 - i, (1023 - (array[i] << 2) | (((array[2] << (i * 2)) & 0xC0) >> 6)) / 1023.0)
        
        return ustruct.unpack('ff', self.buff)
    
    def get_light_sensors(self):
        '''
        The light sensor values on the GiggleBot.

        The lower the values, the darker is the environment around the GiggleBot. It's vice-versa for higher values.

        :returns: A 2-element tuple with the values of the left and right light sensor in this specific order.
        :rtype: tuple(int,int)
        
        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_LIGHT_SENSORS)
        array = self.read(_GIGGLEBOT_ADDRESS, 3)

        for i in b'\x00\x01':
            ustruct.pack_into('f', self.buff, 1 - i, (1023 - (array[i] << 2) | (((array[2] << (i * 2)) & 0xC0) >> 6)) / 1023.0)
        
        return ustruct.unpack('ff', self.buff)
        
    def set_motor_power(self, port, power):
        '''
        Sets the power of a single motor on the GiggleBot.

        :param port: Either :py:attr:`~gigglebot_advanced.MOTOR_LEFT` or :py:attr:`~gigglebot_advanced.MOTOR_RIGHT` depending on which motor has to be controlled.
        :param int power: **-100** to **0** for reverse and from **0** to **100** for full speed ahead.

        '''
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWER + port + ustruct.pack('b', power))
        
    def set_motor_powers(self, powerLeft, powerRight):
        '''
        Sets the power of both motors of the GiggleBot.

        :param int powerLeft: Anywhere between from **-100** to **100** for the left motor.
        :param int powerRight: Anywhere between from **-100** to **100** for the right motor.

        '''
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWERS + ustruct.pack('bb', powerRight, powerLeft))

    def get_motor_status(self, port):
        '''
        Returns a report of the status of a given motor on the GiggleBot.

        :param port: Either :py:attr:`~gigglebot_advanced.MOTOR_LEFT` or :py:attr:`~gigglebot_advanced.MOTOR_RIGHT`.

        This method returns a 2-element list where the 1st element is called the ``status_flag`` and the 2nd one is
        represents the current speed set for the given motor.

        The ``status_flag`` can have the following values:

        * For **0** it means the conditions are normal (the motor can run).
        * For **1** it means the battery voltage is too low or the power switch is off.

        Also, if the battery voltage is **<= 3.3V**, then it's too low and the motors float.
        If the battery voltage is **>= 3.4V**, then it's high enought that the motors are set to run.
        This difference of **0.1V** is introduced in order to prevent the motors from quickly turning on and off if the battery
        voltage is right on the edge.

        :returns: A 2-element list containing the status of the motor and the current speed/power of it.
        :rtype: list(int,int)

        '''
        self.write(_GIGGLEBOT_ADDRESS, _GET_MOTOR_STATUS_LEFT if port == MOTOR_LEFT else _GET_MOTOR_STATUS_RIGHT)
        array = list(bytearray(self.read(_GIGGLEBOT_ADDRESS, 2)))

        if array[1] & 0x80:
            array[1] -= 0x100

        return array

    def reset_all(self):
        '''
        Brings the GiggleBot to a full stop, while also cutting power to the motors, so that the battery life is preserved.
        '''
        self.write(_GIGGLEBOT_ADDRESS, _SET_MOTOR_POWERS + ustruct.pack('bb', _MOTOR_FLOAT, _MOTOR_FLOAT))