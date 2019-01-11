import ustruct
from micropython import const
from microbit import sleep, i2c

# Constants

# BME280 default address.
_ADDR = const(0x76)

# # Operating Modes
# _OSAMPLE_1 = const(1)
# _OSAMPLE_2 = const(2)
# _OSAMPLE_4 = const(3)
# _OSAMPLE_8 = const(4)
# _OSAMPLE_16 = const(5)

# # Standby Settings
# _STANDBY_0p5 = const(0)
# _STANDBY_62p5 = const(1)
# _STANDBY_125 = const(2)
# _STANDBY_250 = const(3)
# _STANDBY_500 = const(4)
# _STANDBY_1000 = const(5)
# _STANDBY_10 = const(6)
# _STANDBY_20 = const(7)

# # Filter Settings
# _FILTER_off = const(0)
# _FILTER_2 = const(1)
# _FILTER_4 = const(2)
# _FILTER_8 = const(3)
# _FILTER_16 = const(4)

# # BME280 Registers
# _REG_DIG_T1 = b'\x88'  # Trimming parameter registers
# _REG_DIG_T2 = b'\x8a'
# _REG_DIG_T3 = b'\x8c'

# _REG_DIG_P1 = b'\x8e'
# _REG_DIG_P2 = b'\x90'
# _REG_DIG_P3 = b'\x92'
# _REG_DIG_P4 = b'\x94'
# _REG_DIG_P5 = b'\x96'
# _REG_DIG_P6 = b'\x98'
# _REG_DIG_P7 = b'\x9a'
# _REG_DIG_P8 = b'\x9c'
# _REG_DIG_P9 = b'\x9e'

# _REG_DIG_H1 = b'\xa1'
# _REG_DIG_H2 = b'\xe1'
# _REG_DIG_H3 = b'\xe3'
# _REG_DIG_H4 = b'\xe4'
# _REG_DIG_H5 = b'\xe5'
# _REG_DIG_H6 = b'\xe6'
# _REG_DIG_H7 = b'\xe7'

# _REG_CHIPID = b'\xd0'
# _REG_VERSION = b'\xd1'
# _REG_SOFTRESET = b'\xe0'

# _REG_STATUS = b'\xf3'
# _REG_CONTROL_HUM = b'\xf2'
# _REG_CONTROL = b'\xf4'
# _REG_CONFIG = b'\xf5'
# #_REG_DATA = b'\xf7'
# _REG_PRESSURE_DATA = b'\xf7'
# _REG_TEMP_DATA     = b'\xfa'
# _REG_HUMIDITY_DATA = b'\xfd'


class TempHumPress(object):
    """
    Class for interfacing with the `Temperature Humidity Pressure Sensor`_.
    """
    
    def __init__(self):
        """
        Constructor for initializing link with the `Temperature Humidity Pressure Sensor`_.

        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        
        self._t_mode = 2 # _OSAMPLE_2
        self._h_mode = 3 # _OSAMPLE_4
        self._p_mode = 3 # _OSAMPLE_4
        
        self._standby = 6 # _STANDBY_10
        self._filter = 3 # _FILTER_8

        self.write = i2c.write
        self.read = i2c.read
        
        # load calibration values.
        self._load_calibration()
        # sleep mode
        self.write(_ADDR, b'\xf4\x24')
        sleep(2)
        
        # set the standby time
        self.write(_ADDR, b'\xf5' + ustruct.pack('B', (self._standby << 5) | (self._filter << 2)))
        sleep(2)
        
        # set the sample modes
        self.write(_ADDR, b'\xf2' + ustruct.pack('B', self._h_mode)) # Set Humidity Oversample
        self.write(_ADDR, b'\xf4' + ustruct.pack('B', (self._t_mode << 5) | (self._p_mode << 2) | 3)) # Set Temp/Pressure Oversample and enter Normal mode
        self._t_fine = 0.0
    
    def _load_calibration(self):
        # Read calibration data
        
        self.write(_ADDR, b'\x88')
        self._dig_T1 = ustruct.unpack('<H', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x8a')
        self._dig_T2 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x8c')
        self._dig_T3 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]

        self.write(_ADDR, b'\x8e')
        self._dig_P1 = ustruct.unpack('<H', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x90')
        self._dig_P2 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x92')
        self._dig_P3 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x94')
        self._dig_P4 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x96')
        self._dig_P5 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x98')
        self._dig_P6 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x9a')
        self._dig_P7 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x9c')
        self._dig_P8 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\x9e')
        self._dig_P9 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        
        self.write(_ADDR, b'\xa1')
        self._dig_H1 = self.read(_ADDR, 1)[0]
        self.write(_ADDR, b'\xe1')
        self._dig_H2 = ustruct.unpack('<h', self.read(_ADDR, 2))[0]
        self.write(_ADDR, b'\xe3')
        self._dig_H3 = ustruct.unpack('b', self.read(_ADDR, 1))[0]
        self.write(_ADDR, b'\xe7')
        self._dig_H6 = ustruct.unpack('b', self.read(_ADDR, 1))[0]
        
        self.write(_ADDR, b'\xe4')
        h4 = ustruct.unpack('b', self.read(_ADDR, 1))[0]
        h4 = (h4 << 4)
        self.write(_ADDR, b'\xe5')
        self._dig_H4 = h4 | (self.read(_ADDR, 1)[0] & 0x0F)
        
        self.write(_ADDR, b'\xe6')
        h5 = ustruct.unpack('b', self.read(_ADDR, 1))[0]
        h5 = (h5 << 4)
        self.write(_ADDR, b'\xe5')
        self._dig_H5 = h5 | (self.read(_ADDR, 1)[0] >> 4 & 0x0F)
    
    def _read_raw_data(self, register):
        # read raw pressure data once it's available
        self.write(_ADDR, b'\xf3')
        while self.read(_ADDR, 1)[0] & 0x08:
            sleep(2)
            self.write(_ADDR, b'\xf3')
        self.write(_ADDR, register)
        return self.read(_ADDR, 3)
    
    def get_temperature_celsius(self):
        """
        Read temperature in Celsius degrees.

        :returns: Temperature in Celsius degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """

        # float in Python is double precision
        data = self._read_raw_data(b'\xfa')
        UT = float(((data[0] << 16) | (data[1] << 8) | data[2]) >> 4)
        var1 = (UT / 16384.0 - float(self._dig_T1) / 1024.0) * float(self._dig_T2)
        var2 = ((UT / 131072.0 - float(self._dig_T1) / 8192.0) * 
            (UT / 131072.0 - float(self._dig_T1) / 8192.0)) * float(self._dig_T3)
        self._t_fine = int(var1 + var2)
        return (var1 + var2) / 5120.0
    
    def get_temperature_fahrenheit(self):
        """
        Read temperature in Fahrenheit degrees.

        :returns: Temperature in Fahrenheit degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return self.get_temperature_celsius() * 1.8 + 32
    
    def get_pressure(self):
        """
        Read the air pressure in pascals.

        :returns: The air pressure in pascals.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        .. note::
            :py:meth:`~thp.get_temperature_celsius` or :py:meth:`~thp.get_temperature_fahrenheit` has to be called in order to update the temperature compensation.

        """
        data = self._read_raw_data(b'\xf7')
        adc = float(((data[0] << 16) | (data[1] << 8) | data[2]) >> 4)
        var1 = float(self._t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(self._dig_P6) / 32768.0
        var2 = var2 + var1 * float(self._dig_P5) * 2.0
        var2 = var2 / 4.0 + float(self._dig_P4) * 65536.0
        var1 = (
               float(self._dig_P3) * var1 * var1 / 524288.0 + float(self._dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(self._dig_P1)
        if var1 == 0:
            return 0
        p = 1048576.0 - adc
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = float(self._dig_P9) * p * p / 2147483648.0
        var2 = p * float(self._dig_P8) / 32768.0
        return p + (var1 + var2 + float(self._dig_P7)) / 16.0

    def get_humidity(self):
        """
        Read the relative humidity as a percentage.

        :returns: Percentage of the relative humidity.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        .. note::
            :py:meth:`~thp.get_temperature_celsius` or :py:meth:`~thp.get_temperature_fahrenheit` has to be called in order to update the temperature compensation.

        """
        data = self._read_raw_data(b'\xfd')
        adc = float((data[0] << 8) | data[1])
        # print 'Raw humidity = {0:d}'.format (adc)
        h = float(self._t_fine) - 76800.0
        h = (adc - (float(self._dig_H4) * 64.0 + float(self._dig_H5) / 16384.0 * h)) * (
        float(self._dig_H2) / 65536.0 * (1.0 + float(self._dig_H6) / 67108864.0 * h * (
        1.0 + float(self._dig_H3) / 67108864.0 * h)))
        h = h * (1.0 - float(self._dig_H1) * h / 524288.0)
        if h > 100:
            h = 100
        elif h < 0:
            h = 0
        return h
    
    def get_dewpoint_celsius(self):
        """
        Read dewpoint temperature in Celsius degrees.
        
        The dewpoint represents the atmospheric temperature (varying according to pressure and humidity)
        below which water droplets begin to condense and dew can form.

        :returns: Dewpoint temperature in Celsius degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        # Return calculated dewpoint in C, only accurate at > 50% RH
        return self.get_temperature_celsius() - ((100 - self.get_humidity()) / 5)
    
    def get_dewpoint_fahrenheit(self):
        """
        Read dewpoint temperature in Fahrenheit degrees.
        
        It does the exact same thing as :py:meth:`~thp.TempHumPress.get_dewpoint_celsius`, the only difference being the used unit of measure.

        :returns: Dewpoint temperature in Fahrenheit degrees degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        # Return calculated dewpoint in F, only accurate at > 50% RH
        return self.get_dewpoint_celsius() * 1.8 + 32
    
    def get_pressure_inches(self):
        """
        Read pressure in inches of Hg.

        :returns: The air pressure in inches of Hg.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        .. note::
            :py:meth:`~thp.get_temperature_celsius` or :py:meth:`~thp.get_temperature_fahrenheit` has to be called in order to update the temperature compensation.

        """
        # Wrapper to get pressure in inches of Hg
        return self.get_pressure() * 0.0002953
