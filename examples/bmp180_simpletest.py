# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import busio
import bmp180

i2c = busio.I2C(board.SCL, board.SDA)
bmp180 = bmp180.BMP180_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp180.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % bmp180.temperature)
    print("Pressure: %0.1f hPa" % bmp180.pressure)
    print("Altitude = %0.2f meters" % bmp180.altitude)
    time.sleep(2)
