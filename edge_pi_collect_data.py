import time
import board
import adafruit_bh1750
from time import sleep
from picamera import PiCamera
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import sensorLoggingDelay, imageCaptureDelay
from config import datadir, edgePiCSVFilename, edgePiImagesDirectory, edgePiImageFilenameFormat
import pandas as pd

'''
Python program to take pictures from the picamera and collect light intensity from
the bh1750 sensor connected to the edge Pis every 10 minutes

edge pi data output
directory containing images with filenames containing the date and time they were taken
csv file containing datetime and light intensity
'''

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)
camera = PiCamera()
# set picamera resolution to 5mp if 8mp is not supported
try:
    camera.resolution = (3280, 2464)
except Exception as err:
    camera.resolution = (2592, 1944)

columns = pd.read_csv(datadir + edgePiCSVFilename).columns.values
print(columns)

def logData():
    lightintensity = sensor.lux
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), lightintensity]]
    print(data)
    df = pd.DataFrame(data, columns=columns)
    print(df)
    df.to_csv(datadir+edgePiCSVFilename, mode='a', index=False, header=False)

# timedeltas for sensor logging and image capture
sensorLoggingTimeDelta = timedelta(seconds=sensorLoggingDelay)
imageCaptureTimeDelta = timedelta(seconds=imageCaptureDelay)
lastSensorLogTime = datetime.now()
lastImageCaptureTime = datetime.now()

logData()
print('logging started')
while True:
    if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
        lastSensorLogTime = datetime.now()
        logData()

    if datetime.now() - lastImageCaptureTime >= sensorLoggingTimeDelta:
        lastImageCaptureTime = datetime.now()
        hour = datetime.now().time().hour
        if hour >= 6 and hour <= 18:
            print('image captured')
            camera.capture(edgePiImagesDirectory + edgePiImageFilenameFormat.format \
            (datetime=datetime.now().strftime('%Y%m%d_%H%M%S'), uname=uname, sitename=sitename))
