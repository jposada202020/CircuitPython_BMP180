# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import bmp180

i2c = board.I2C()
bmp = bmp180.BMP180(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % bmp.temperature)
    print("Pressure: %0.1f hPa" % bmp.pressure)
    print("Altitude = %0.2f meters" % bmp.altitude)
    time.sleep(2)
