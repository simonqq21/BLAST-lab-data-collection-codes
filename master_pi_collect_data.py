import time
from adafruit_bme280 import basic as adafruit_bme280
import board
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import loggingDuration
from config import datadir, masterPiCSVFilename
import pandas as pd

'''
Python program to collect temperature, humidity, and pressure from the BME280 sensor
connected to the master Pi every 10 minutes

master pi data output
csv file containing datetime, temperature, humidity, and pressure
'''

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

columns = pd.read_csv(datadir + masterPiCSVFilename).columns.values
print(columns)
lastLogTime = datetime.now()

def logData():
    lastLogTime = datetime.now()
    temperature = bme280.temperature
    pressure = bme280.pressure
    humidity = bme280.relative_humidity
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), temperature, pressure, humidity]]
    print(data)
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(masterPiCSVFilename, mode='a', index=False, header=False)

logData()
print('logging started')
while True:
    if datetime.now() - lastLogTime >= timedelta(seconds=loggingDuration):
        logData()
