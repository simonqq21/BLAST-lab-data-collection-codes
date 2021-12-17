import board
import time
from adafruit_bme280 import basic as adafruit_bme280
from datetime import datetime, date, time, timedelta
from config import loggingDuration, csvfilename

'''
Python program to collect temperature, humidity, and pressure from the BME280 sensor
connected to the master Pi every 10 minutes
'''

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
print()

bme280.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" %bme280.temperature)
    print("Humidity: %0.1f %%" %bme280.relative_humidity)
    print("Pressure: %0.1f hPa" %bme280.pressure)
    print("Altitude = %0.2f meters" %bme280.altitude)
    time.sleep(2)
