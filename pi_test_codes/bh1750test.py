import time
import board
import adafruit_bh1750

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

while True:
    print("%.2f Lux"%sensor.lux)
    time.sleep(1)
