import time
# import board
# import adafruit_bh1750
from time import sleep
# from picamera import PiCamera
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import sensorLoggingDelay, imageCaptureDelay
from config import datadir, edgePiCSVFilename, edgePiImagesDirectory, edgePiImageFilenameFormat
import pandas as pd
import paho.mqtt.client as mqtt
import json

'''
Python program to take pictures from the picamera and collect light intensity from
the bh1750 sensor connected to the edge Pis every 10 minutes

edge pi data output
directory containing images with filenames containing the date and time they were taken
REST API for sending images to server
csv file containing datetime and light intensity
mqtt publish with the data above
'''

# i2c = board.I2C()
# sensor = adafruit_bh1750.BH1750(i2c)
# camera = PiCamera()
# set picamera resolution to 5mp if 8mp is not supported
# try:
#     camera.resolution = (3280, 2464)
# except Exception as err:
#     camera.resolution = (2592, 1944)

columns = pd.read_csv(datadir + edgePiCSVFilename).columns.values
print(columns)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # if msg.topic == "t1/t2":
    #     payload = json.loads(msg.payload)
    #     print(payload)

def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client(f"{sitename}_{uname}")
publish_topic = f"/shift/DLSAU/edge-pi1/sensorvalues"
# publish_topic = f"/shift/{sitename}/{uname}/sensorvalues"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# client.connect("103.231.240.146", 11000)
client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(client)
print(publish_topic)
client.loop_start()

lightintensity = 100
def logData():
    global lightintensity
    # lightintensity = sensor.lux
    lightintensity += 1
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), lightintensity]]
    print(data)
    df = pd.DataFrame(data, columns=columns)
    print(df)
    jsonData = df.to_json()
    client.publish(publish_topic, jsonData)
    df.to_csv(datadir+edgePiCSVFilename, mode='a', index=False, header=False)

def capture_image():
    print('image captured')
    # camera.capture(edgePiImagesDirectory + edgePiImageFilenameFormat.format \
    # (datetime=datetime.now().strftime('%Y%m%d_%H%M%S'), uname=uname, sitename=sitename))

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
            capture_image()
