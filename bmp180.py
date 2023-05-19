# SPDX-FileCopyrightText: Copyright (c) 2020 BadTigrou, 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""
`bmp180` - Temperature & Barometric Pressure Sensor
===============================================================================

CircuitPython driver from BMP180 Temperature and Barometric Pressure sensor

* Author(s): BadTigrou, Jose D. Montoya
"""


from time import sleep
from micropython import const
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct, Struct
from adafruit_bus_device import i2c_device

try:
    from busio import I2C
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_BMP180.git"

_CHIP_ID = const(0x255)
_I2C_ADDR = const(0x77)

_REGISTER_CHIPID = const(0xD0)
_REGISTER_SOFTRESET = const(0xE0)
_REGISTER_CONTROL = const(0xF4)
_REGISTER_DATA = const(0xF6)
_REGISTER_AC1 = const(0xAA)

"""oversampling values for temperature, pressure, and humidity"""
TEMPERATURE_CMD = const(0x2E)
PRESSURE_OVERSAMPLING_X1 = const(0x01)
PRESSURE_OVERSAMPLING_X2 = const(0x02)
PRESSURE_OVERSAMPLING_X4 = const(0x03)
PRESSURE_OVERSAMPLING_X8 = const(0x04)

_BMP180_PRESSURE_CMD = {
    PRESSURE_OVERSAMPLING_X1: 0x34,
    PRESSURE_OVERSAMPLING_X2: 0x74,
    PRESSURE_OVERSAMPLING_X4: 0xB4,
    PRESSURE_OVERSAMPLING_X8: 0xF4,
}

"""mode values"""
MODE_ULTRALOWPOWER = const(0x00)
MODE_STANDARD = const(0x01)
MODE_HIGHRES = const(0x02)
MODE_ULTRAHIGHRES = const(0x03)

_BMP180_MODES = (MODE_ULTRALOWPOWER, MODE_STANDARD, MODE_HIGHRES, MODE_ULTRAHIGHRES)


class BMP180:
    """Driver for the BMP180 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the BMP180 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x77`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`BMP180` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import bmp180

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        bmp = bmp180.BMP180(i2c)

    Now you have access to the attributes

    .. code-block:: python

        press = bmp.pressure
        temp = bmp.temperature

    """

    _device_id = ROUnaryStruct(_REGISTER_CHIPID, "H")
    _reg_control = UnaryStruct(_REGISTER_CONTROL, "H")
    _reg_soft_reset = UnaryStruct(_REGISTER_SOFTRESET, "H")
    _regdata_MSB = UnaryStruct(_REGISTER_DATA, "H")
    _regdata_LSB = UnaryStruct(_REGISTER_DATA + 1, "H")
    _regdata_XLSB = UnaryStruct(_REGISTER_DATA + 2, "H")

    _coeffs = Struct(_REGISTER_AC1, ">hhhHHHhhhhh")
    _raw_temperature = UnaryStruct(_REGISTER_DATA, ">H")

    def __init__(self, i2c_bus: I2C, address: int = 0x77) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != _CHIP_ID:
            raise RuntimeError(
                "Failed to find BMP180! Chip ID {}".format(self._device_id)
            )

        self._oversampling_setting = PRESSURE_OVERSAMPLING_X8
        self._mode = MODE_HIGHRES
        self.coeffs_mem = self._coeffs
        self.sea_level_pressure = 1013.25

    def _reset(self):
        """Soft reset the sensor"""
        self._reg_soft_reset = 0xB6  # reset the device
        sleep(0.004)  # Datasheet says 2ms.  Using 4ms just to be safe

    @property
    def temperature(self):
        """
        The compensated temperature in Celsius.
        Calculation of true temperature in steps of 0.1°C.
        """
        self._reg_control = TEMPERATURE_CMD
        sleep(0.005)  # Wait 5ms
        UT = self._raw_temperature
        X1 = ((UT - self.coeffs_mem[5]) * self.coeffs_mem[4]) / 2**15.0
        X2 = (self.coeffs_mem[9] * 2**11.0) / (X1 + self.coeffs_mem[10])
        B5 = X1 + X2
        temp = ((B5 + 8) / 2**4.0) / 10.0
        return temp

    @property
    def altitude(self):
        """
        With the measured pressure p and the pressure at sea level p0 e.g. 1013.25hPa,
        the altitude in meters can be calculated with the international barometric formula

        With the measured pressure p and the absolute altitude the pressure at sea level
        can be calculated too. See the altitude setter for this calculation
        """
        altitude = 44330.0 * (
            1.0 - ((self.pressure / self.sea_level_pressure) ** 0.19025)
        )
        return round(altitude, 1)

    @altitude.setter
    def altitude(self, value: float) -> None:
        self.sea_level_pressure = self.pressure / (1.0 - value / 44330.0) ** 5.255

    @property
    def pressure(self):
        """
        The compensated pressure in hectoPascals.
        Calculation of true  pressure in steps of 1Pa (= 0.01hPa = 0.01mbar)
        """
        self._reg_control = TEMPERATURE_CMD
        sleep(0.005)  # Wait 5ms
        UT = self._raw_temperature
        UP = self._read_raw_pressure()

        X1 = ((UT - self.coeffs_mem[5]) * self.coeffs_mem[4]) / 2**15.0
        X2 = (self.coeffs_mem[9] * 2**11.0) / (X1 + self.coeffs_mem[10])
        B5 = X1 + X2
        B6 = B5 - 4000
        X1 = (self.coeffs_mem[7] * (B6 * B6) / 2**12.0) / 2**11.0
        X2 = (self.coeffs_mem[1] * B6) / 2**11.0
        X3 = X1 + X2
        B3 = (((self.coeffs_mem[0] * 4 + X3) * 2 ** float(self._mode)) + 2) / 4
        X1 = (self.coeffs_mem[2] * B6) / 2**13.0
        X2 = (self.coeffs_mem[6] * ((B6 * B6) / 2**12.0)) / 2**16.0
        X3 = ((X1 + X2) + 2) / 2**2.0
        B4 = (self.coeffs_mem[3] * (X3 + 32768.0)) / 2**15.0
        B7 = (UP - B3) * (50000 / 2 ** float(self._mode))

        if B7 < 2147483648.0:
            press = (B7 * 2) / B4
        else:
            press = (B7 / B4) * 2

        X1 = (press / 2**8.0) * (press / 2**8.0)
        X1 = (X1 * 3038) / 2**16.0
        X2 = (-7357 * press) / 2**16.0

        return (press + ((X1 + X2 + 3791) / 2**4.0)) / 100

    def _read_raw_pressure(self):

        self._reg_control = _BMP180_PRESSURE_CMD[self._mode]

        if self._mode == PRESSURE_OVERSAMPLING_X8:
            sleep(0.026)
        elif self._mode == PRESSURE_OVERSAMPLING_X4:
            sleep(0.014)
        elif self._mode == PRESSURE_OVERSAMPLING_X2:
            sleep(0.008)
        else:
            sleep(0.005)

        msb = self._regdata_MSB & 0xFF
        lsb = self._regdata_LSB & 0xFF
        xlsb = self._regdata_XLSB & 0xFF

        return ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)

    @property
    def mode(self):
        """
        Operation mode

        +----------------------------------------+-------------------------+
        | Mode                                   | Value                   |
        +========================================+=========================+
        | :py:const:`bmp180.MODE_ULTRALOWPOWER`  | :py:const:`0x00`        |
        +----------------------------------------+-------------------------+
        | :py:const:`bmp180.MODE_STANDARD`       | :py:const:`0x01`        |
        +----------------------------------------+-------------------------+
        | :py:const:`bmp180.MODE_HIGHRES`        | :py:const:`0x02`        |
        +----------------------------------------+-------------------------+
        | :py:const:`bmp180.MODE_ULTRAHIGHRES`   | :py:const:`0x03`        |
        +----------------------------------------+-------------------------+

        Example
        ---------------------

        .. code-block:: python

            i2c = board.I2C()
            qmc = bmp180.BMP180(i2c)


            bmp180.mode = bmp180.MODE_HIGHRES

        """
        return self._mode

    @mode.setter
    def mode(self, value):

        if value not in _BMP180_MODES:
            raise ValueError("Mode {} not supported".format(value))
        self._mode = value

    @property
    def oversampling_setting(self):
        """
        Oversampling setting
        Allowed values are set in the OVERSAMPLES enum class
        """
        return self._oversampling_setting

    @oversampling_setting.setter
    def oversampling_setting(self, value):
        if not value in _BMP180_PRESSURE_CMD:
            raise ValueError("Overscan value {} not supported".format(value))
        self._oversampling_setting = value
