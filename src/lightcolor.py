import ustruct
from micropython import const
from microbit import sleep, i2c

# # Constants
# _COMMAND_BIT     = 0x80
# _ENABLE           = 0x00
# _ENABLE_AIEN      = 0x10 # RGBC Interrupt Enable
# _ENABLE_WEN       = 0x08 # Wait enable - Writing 1 activates the wait timer
# _ENABLE_AEN       = 0x02 # RGBC Enable - Writing 1 actives the ADC, 0 disables it
# _ENABLE_PON       = 0x01 # Power on - Writing 1 activates the internal oscillator, 0 disables it
# _ATIME            = 0x01 # Integration time
# _WTIME            = 0x03 # Wait time (if ENABLE_WEN is asserted)
# _AILTL            = 0x04 # Clear channel lower interrupt threshold
# _AILTH            = 0x05
# _AIHTL            = 0x06 # Clear channel upper interrupt threshold
# _AIHTH            = 0x07
# _PERS             = 0x0C # Persistence register - basic SW filtering mechanism for interrupts
# _PERS_NONE        = 0b0000 # Every RGBC cycle generates an interrupt
# _PERS_1_CYCLE     = 0b0001 # 1 clean channel value outside threshold range generates an interrupt
# _PERS_2_CYCLE     = 0b0010 # 2 clean channel values outside threshold range generates an interrupt
# _PERS_3_CYCLE     = 0b0011 # 3 clean channel values outside threshold range generates an interrupt
# _PERS_5_CYCLE     = 0b0100 # 5 clean channel values outside threshold range generates an interrupt
# _PERS_10_CYCLE    = 0b0101 # 10 clean channel values outside threshold range generates an interrupt
# _PERS_15_CYCLE    = 0b0110 # 15 clean channel values outside threshold range generates an interrupt
# _PERS_20_CYCLE    = 0b0111 # 20 clean channel values outside threshold range generates an interrupt
# _PERS_25_CYCLE    = 0b1000 # 25 clean channel values outside threshold range generates an interrupt
# _PERS_30_CYCLE    = 0b1001 # 30 clean channel values outside threshold range generates an interrupt
# _PERS_35_CYCLE    = 0b1010 # 35 clean channel values outside threshold range generates an interrupt
# _PERS_40_CYCLE    = 0b1011 # 40 clean channel values outside threshold range generates an interrupt
# _PERS_45_CYCLE    = 0b1100 # 45 clean channel values outside threshold range generates an interrupt
# _PERS_50_CYCLE    = 0b1101 # 50 clean channel values outside threshold range generates an interrupt
# _PERS_55_CYCLE    = 0b1110 # 55 clean channel values outside threshold range generates an interrupt
# _PERS_60_CYCLE    = 0b1111 # 60 clean channel values outside threshold range generates an interrupt
# _CONFIG           = 0x0D
# _CONFIG_WLONG     = 0x02 # Choose between short and long (12x) wait times via WTIME
# _CONTROL          = 0x0F # Set the gain level for the sensor
# _ID               = 0x12 # 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
# _STATUS           = 0x13
# _STATUS_AINT      = 0x10 # RGBC Clean channel interrupt
# _STATUS_AVALID    = 0x01 # Indicates that the RGBC channels have completed an integration cycle

# _CDATAL           = 0x14 # Clear channel data
# _CDATAH           = 0x15
# _RDATAL           = 0x16 # Red channel data
# _RDATAH           = 0x17
# _GDATAL           = 0x18 # Green channel data
# _GDATAH           = 0x19
# _BDATAL           = 0x1A # Blue channel data
# _BDATAH           = 0x1B

_ADDR            = const(0x29)
GAIN_1X          = 0x00 #  1x gain
GAIN_4X          = 0x01 #  4x gain
GAIN_16X         = 0x02 # 16x gain
GAIN_60X         = 0x03 # 60x gain

class LightColorSensor(object):
    """
    Class for interfacing with the `Light and Color Sensor`_.
    """

    def __init__(self, integration_time=0.0048, gain=GAIN_16X):
        """
        Constructor to initialize the `Light and Color Sensor`_.

        :param float integration_time = 0.0024: Time in seconds for each sample. **0.0024** second (2.4*ms*) increments. Clipped to the range of **0.0024** to **0.6144** *seconds*.
        :param int gain = GAIN_16X: The gain constant. Valid values are ``lightcolor.GAIN_1X``, ``lightcolor.GAIN_4X``, ``lightcolor.GAIN_16X`` and ``lightcolor.GAIN_60X``.
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        
        self.write = i2c.write
        self.read = i2c.read

        # check we have the proper sensor
        self.write(_ADDR, b'\x92')
        if self.read(_ADDR, 1)[0] != 0x44:
            raise RuntimeError('Incorrect chip ID.')

        # set integration time
        val = int(0x100 - (integration_time / 0.0024))
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        self.write(_ADDR, b'\x81' + ustruct.pack('B', val))
        self.integration_time_val = val
        
        # set gain.
        self.write(_ADDR, b'\x8f' + ustruct.pack('B', gain))
        
        # Enable the device (by default, the device is in power down mode on bootup).
        self.write(_ADDR, b'\x80\x01')
        sleep(0.01)
        self.write(_ADDR, b'\x80\x03')

    def set_led(self, value, delay=True):
        """
        Turn on/off the LED on the `Light and Color Sensor`_.

        :param bool value: ``True`` for turning it on or ``False`` otherwise.
        :param bool delay = True: Whether to wait for that much as it takes to take a reading before actually reading the sensor.
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        For things that emit light like monitors, the LED should be turned off, but for anything else it is recommended to have it turned on.
        """

        # old set_interrupt function
        self.write(_ADDR, b'\x8c\x00')
        self.write(_ADDR, b'\x80')
        enable = self.read(_ADDR, 1)[0]
        if value:
            enable |= 0x10
        else:
            enable &= ~0x10
        self.write(_ADDR, b'\x80' + ustruct.pack('B', enable))

        if delay:
            sleep((256 - self.integration_time_val) * 0.0024 * 2) 

    def get_color(self):
        """
        Read the sensor and determine which color it resembles the most from the :py:attr:`~lightcolor.known_colors` list.

        This method is based off of :py:func:`~lightcolor.guess_color_hsv` function.

        :returns: The detected color in string format and then a 3-element tuple describing the color in RGB format. The values of the RGB tuple are between **0** and **255**.
        :rtype: tuple(str,(float,float,float))
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return guess_color_hsv(self.get_raw_data(delay=True))

    def get_raw_data(self, delay=True):
        """
        Read the **RGBA** values from the sensor.
        
        :param bool delay = True: Whether to add delay before actually reading the sensor or not. The delay is equal to length of time it takes to take a reading.
        :returns: The RGBA values as a 4-tuple on a scale of 0-1.
        :rtype: tuple(float,float,float,float)
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        if delay:
            # Delay for the integration time to allow reading immediately after the previous read.
            sleep(((256 - self.integration_time_val) * 0.0024))
        div = ((256 - self.integration_time_val) * 1024)
        
        # Read each color register.
        self.write(_ADDR, b'\x96')
        r = ustruct.unpack('<H', self.read(_ADDR, 2))[0] / div
        self.write(_ADDR, b'\x98')
        g = ustruct.unpack('<H', self.read(_ADDR, 2))[0] / div
        self.write(_ADDR, b'\x9a')
        b = ustruct.unpack('<H', self.read(_ADDR, 2))[0] / div
        self.write(_ADDR, b'\x94')
        c = ustruct.unpack('<H', self.read(_ADDR, 2))[0] / div
        if r > 1:
            r = 1
        if g > 1:
            g = 1
        if b > 1:
            b = 1
        if c > 1:
            c = 1

        return (r, g, b, c)

#: 12 predefined colors in RGB format that the :py:class:`~lightcolor.LightColorSensor` class and :py:func:`~lightcolor.guess_color_hsv`
#: function use to detect colors.
known_colors = {
    "red": (255, 0, 0),
    "orange": (255, 128, 0),
    "yellow": (255, 255, 0),
    "chartreuse-green": (128, 255, 0),
    "green": (0, 255, 0),
    "spring-green": (0, 255, 128),
    "cyan": (0, 255, 255),
    "azure": (0, 128, 255),
    "blue": (0, 0, 255),
    "violet": (127, 0, 255),
    "magenta": (255, 0, 255),
    "rose": (255, 0, 127)
}

#: The same 12 predefined colors in :py:attr:`~lightcolor.known_colors`, but in HSV format. Used by 
#: :py:class:`~lightcolor.LightColorSensor` class and :py:func:`~lightcolor.guess_color_hsv` function to
#: detect colors.
known_hsv = {
    "red": [(-13, 65, 40), ( 17, 100, 100)],
    "orange": [( 18, 65, 40), ( 47, 100, 100)],
    "yellow": [( 48, 65, 40), ( 76, 100, 100)],
    "chartreuse-green": [( 77, 65, 40), (105, 100, 100)],
    "green": [(106, 65, 40), (136, 100, 100)],
    "spring-green": [(137, 65, 40), (166, 100, 100)],
    "cyan": [(167, 65, 40), (194, 100, 100)],
    "azure": [(195, 65, 40), (222, 100, 100)],
    "blue": [(223, 65, 40), (256, 100, 100)],
    "violet": [(257, 65, 40), (286, 100, 100)],
    "magenta": [(288, 65, 40), (316, 100, 100)],
    "rose": [(317, 65, 40), (346, 100, 100)]
}

def translate_to_hsv(in_color):
    """
    Standard algorithm to switch from one color system (**RGB**) to another (**HSV**).

    :param tuple(float,float,float) in_color: The RGB tuple list that gets translated to HSV system. The values of each element of the tuple is between **0** and **1**.
    :return: The translated HSV tuple list. Returned values are *H(0-360)*, *S(0-100)*, *V(0-100)*.
    :rtype: tuple(int, int, int)

    .. important::
        For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
        please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.

    """
    r,g,b = in_color

    min_channel = min((r,g,b))
    max_channel = max((r,g,b))

    v = max_channel
    delta = max_channel - min_channel
    if delta < 0.0001:
        s = 0
        h = 0
    else:
        if max_channel > 0:
            s = delta / max_channel
            if r >= max_channel:
                h = (g - b) / delta
            elif g >= max_channel:
                h = 2.0 + (b - r) / delta
            else:
                h = 4 + (r - g ) / delta

            h = h * 60
            if h < 0:
                h = h + 360

        else:
            s = 0
            h = 0

    return (h, s * 100, v * 100)

def guess_color_hsv(in_color):
    """
    Determines which color ``in_color`` parameter is closest to in the :py:attr:`~lightcolor.known_colors` list.

    This function converts the RGBA input into an HSV representation and then it determines within which color boundary described in :py:attr:`~lightcolor.known_hsv` dictionary it fits in.
    Afterwards, it returns the candidate color in both text and RGB formats.

    :param tuple(float,float,float,float) in_color: A 4-element tuple list for the *Red*, *Green*, *Blue* and *Alpha* channels. The elements are all valued between **0** and **1**.
    :returns: The detected color in string format and then a 3-element tuple describing the color in RGB format. The values of the RGB tuple are between **0** and **255**.
    :rtype: tuple(str,(float,float,float))

    .. important::
        For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
        please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.

    """

    r,g,b,c = in_color
    # print("incoming: {} {} {} {}".format(r,g,b,c))

    # handle black
    # luminosity is too low, or all color readings are too low
    if c < 0.04 or (r/c < 0.10 and g/c < 0.10 and b/c < 0.10):
        return ("black",(0,0,0))

    # handle white
    # luminosity is high, or all color readings are high
    if c > 0.95 or (r/c > 0.9 and g/c > 0.9 and b/c > 0.9):
        return ("white",(255,255,255))

    # divide by luminosity(clarity) to minimize variations
    h,s,v = translate_to_hsv((r, g, b))

    # another black is possible
    # black has a value of 0 and a saturation of 100
    # values of 15 and 95 chosen randomly. They may need to be tweaked
    if v < 15 and s > 95:
        return ("black", (0,0,0))

    # so is another white
    # white has a value of 100 and a saturation of 0
    # values of 95 and 10 chosen randomly. They may need to be tweaked
    if v > 95 and s < 10:
        return ("white", (255,255,255))

    for key, value in known_hsv.items():
        if h >= value[0][0] and h <= value[1][0]:
            return (key, known_colors[key])
