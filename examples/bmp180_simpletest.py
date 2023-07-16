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
    print(f"Temperature: {bmp.temperature:.1f} °C")
    print(f"Pressure: {bmp.pressure:.1f} hPa")
    print(f"Altitude: {bmp.altitude:.1f} mts")
    print("")
    time.sleep(2)
