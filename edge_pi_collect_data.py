import time
import board
import adafruit_bh1750
from time import sleep
from picamera import PiCamera
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import sensorLoggingDelay, imageCaptureDelay
from config import csvDir, csvfilename, edgePiImgDir, edgePiImageFilenameFormat
from config import sensorPublishTopic, cameraPublishTopic, mqttIP, mqttPort
import pandas as pd
import paho.mqtt.client as mqtt
import json
from io import BytesIO
import binascii

'''
Python program to take pictures from the picamera and collect light intensity from
the bh1750 sensor connected to the edge Pis every 10 minutes

edge pi data output
directory containing images with filenames containing the date and time they were taken
REST API for sending images to server
csv file containing datetime and light intensity
mqtt publish with the data above

/shift/<sitename>/<hostname>/sensorvalues

/shift/dlsau/dlsau-dft0master-1/sensorvalues

/shift/dlsau/dlsau-dft0edge-3/sensorvalues
/shift/dlsau/dlsau-kratky0edge-1/sensorvalues
/shift/dlsau/dlsau-dft0edge-1/sensorvalues
/shift/dlsau/dlsau-dft0edge-2/sensorvalues
/shift/dlsau/dlsau-kratky0edge-2/sensorvalues

/shift/dlsau/dlsau-dft0edge-3/images
/shift/dlsau/dlsau-kratky0edge-1/images
/shift/dlsau/dlsau-dft0edge-1/images
/shift/dlsau/dlsau-dft0edge-2/images
/shift/dlsau/dlsau-kratky0edge-2/images


...
send json string of all sensor values
'''

try:
    i2c = board.I2C()
    sensor = adafruit_bh1750.BH1750(i2c)
except:
    sensor = None
try:
    camera = PiCamera()
    # set picamera resolution to 5mp if 8mp is not supported
    try:
        camera.resolution = (3280, 2464)
    except Exception as err:
        camera.resolution = (2592, 1944)
except:
    pass

columns = pd.read_csv(csvDir + csvfilename).columns.values
print(columns)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic)

def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client(f"{sitename}_{uname}")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(mqttIP, mqttPort)
# client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(client)
print(sensorPublishTopic)
print(cameraPublishTopic)
client.loop_start()

# BytesIO for pi camera image
imageStream = BytesIO()

lightintensity = 0
def logData():
    global lightintensity
    lightintensity = 999999999
    if sensor is not None:
        lightintensity = sensor.lux
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), sitename, uname, lightintensity]]
    df = pd.DataFrame(data, columns=columns)
    jsonData = df.to_json()
    try:
        client.publish(sensorPublishTopic, jsonData)
    except:
        print("Publish failed, check broker")
    df.to_csv(csvDir + csvfilename, mode='a', index=False, header=False)

# def sendStreamViaMQTT(bIO):
#     client.publish(cameraPublishTopic, bIO.read(), 0)

def captureImage():
    global imageStream
    print('image captured')
    filename = edgePiImageFilenameFormat.format \
    (datetime=datetime.now().strftime('%Y%m%d_%H%M%S'), uname=uname, sitename=sitename)
    camera.capture(edgePiImgDir + filename)
    sleep(1)
    camera.capture(imageStream, 'jpeg')
    image_data = binascii.b2a_base64(imageStream.getvalue()).decode()
    data = {'filename': filename, 'hostname': uname, 'image_data': image_data}
    jsondata = json.dumps(data)
    try:
        client.publish(cameraPublishTopic, jsondata, 0)
    except:
        print("Publish failed, check broker")

# timedeltas for sensor logging and image capture
sensorLoggingTimeDelta = timedelta(seconds=sensorLoggingDelay)
imageCaptureTimeDelta = timedelta(seconds=imageCaptureDelay)
lastSensorLogTime = datetime.now()
lastImageCaptureTime = datetime.now()

logData()
captureImage()
print('logging started')
while True:
    if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
        lastSensorLogTime = datetime.now()
        logData()

    if datetime.now() - lastImageCaptureTime >= imageCaptureTimeDelta:
        lastImageCaptureTime = datetime.now()
        hour = datetime.now().time().hour
        if hour >= 6 and hour <= 18:
            captureImage()
