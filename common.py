import os

import time
from time import sleep
from datetime import datetime, date, time, timedelta

from config import SITENAME, HOSTNAME, ROLE
from config import sensorLoggingDelay, imageCaptureDelay
from config import csvDir, csvfilename, edgePiImgDir, edgePiImageFilenameFormat
from config import sensorPublishTopic, cameraPublishTopic, mqttIP, mqttPort

import pandas as pd
import paho.mqtt.client as mqtt
import json
from io import BytesIO
import binascii
from sensors import BH1750init, piCameraInit, BME280init
from sensors import BH1750Read, BME280Read, piCameraCapture

'''
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

# create path if not exists
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def edgePiCollectData():
    try:
        bh1750 = BH1750init()
    except:
        print("bh1750 sensor error")
    try:
        camera = piCameraInit()
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
    client = mqtt.Client(f"{SITENAME}_{HOSTNAME}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    try:
        client.connect(mqttIP, mqttPort)
        print(client)
        print(sensorPublishTopic)
        print(cameraPublishTopic)
        client.loop_start()
    except:
        print("Failed to connect to broker!")

    def logData():
        lightintensity = BH1750Read(bh1750)
        data = [['edge', datetime.now().strftime('%m/%d/%Y %H:%M'), SITENAME, HOSTNAME, lightintensity]]
        df = pd.DataFrame(data, columns=columns)
        print(df)
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
        (datetime=datetime.now().strftime('%Y%m%d_%H%M%S'), hostname=HOSTNAME, sitename=SITENAME)
        imageStream = piCameraCapture(camera, edgePiImgDir + filename)
        image_data = binascii.b2a_base64(imageStream.getvalue()).decode()
        data = {'role': 'edge', 'filename': filename, 'hostname': HOSTNAME, 'image_data': image_data}
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
        try:
            if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
                lastSensorLogTime = datetime.now()
                logData()

            if datetime.now() - lastImageCaptureTime >= imageCaptureTimeDelta:
                lastImageCaptureTime = datetime.now()
                hour = datetime.now().time().hour
                if hour >= 6 and hour <= 18:
                    captureImage()
        except Exception as e:
            logFile = open("logger.log", "a")
            logFile.write(str(e))


def masterPiCollectData():
    try:
        bme280 = BME280init()
    except:
        print("bme280 sensor error")

    # get columns from file
    columns = pd.read_csv(csvDir + csvfilename).columns.values
    print(columns)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(client, userdata, msg):
        print(msg.topic)
        # print(msg.topic + " " + str(msg.payload))

    def on_publish(client, userdata, mid):
        print("Message published")

    # mqtt client init
    client = mqtt.Client(f"{SITENAME}_{HOSTNAME}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    try:
        client.connect(mqttIP, mqttPort)
        print(client)
        print(sensorPublishTopic)
        client.loop_start()
    except:
        print("Publish failed, check broker")

    def logData():
        temperature, pressure, humidity = BME280Read(bme280)
        data = [['master', datetime.now().strftime('%m/%d/%Y %H:%M'), SITENAME, HOSTNAME, temperature, pressure, humidity]]
        print(data)
        df = pd.DataFrame(data, columns=columns)
        print(df)
        jsonData = df.to_json()
        try:
            client.publish(sensorPublishTopic, jsonData)
        except:
            print("Publish failed, check broker")
        df.to_csv(csvDir + csvfilename, mode='a', index=False, header=False)

    # timedelta for sensor logging
    sensorLoggingTimeDelta = timedelta(seconds=sensorLoggingDelay)
    lastSensorLogTime = datetime.now()

    logData()
    print('logging started')
    while True:
        try:
            if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
                lastSensorLogTime = datetime.now()
                logData()
        except Exception as e:
            logFile = open("logger.log", "a")
            logFile.write(str(e))
