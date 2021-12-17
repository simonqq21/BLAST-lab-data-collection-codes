import time
import board
import adafruit_bh1750
from time import sleep
from picamera import PiCamera

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)
camera = PiCamera()
camera.resolution = (1024, 768)

sleep(2)
camera.capture('sample.jpg')

while True:
    print("%.2f Lux"%sensor.lux)
    time.sleep(1)
