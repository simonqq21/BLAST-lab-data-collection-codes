import time
from time import sleep
from datetime import datetime, date, time, timedelta
import paho.mqtt.client as mqtt
import json
from io import BytesIO
import binascii

sitename = 'dlsau'
uname = 'testpi'
cameraPublishTopic = '/shift/dlsau/testpi/images'
mqttIP = "mqtt.eclipseprojects.io"
mqttPort = 1883
# mqttIP = "103.231.240.146"
# mqttPort = 11000

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_publish(client, userdata, mid):
    print(userdata)
    print("Message published")

# mqtt client init
client = mqtt.Client(f"{sitename}_{uname}")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(mqttIP, mqttPort)
print(cameraPublishTopic)
client.loop_start()

# BytesIO for pi camera image
imageStream = BytesIO()

filenameNumber = 0
def captureImage():
    global imageStream, filenameNumber
    print('image captured')
    with open("sample_image.jpg", "rb") as f:
        imageStream = BytesIO(f.read())
    filename = f'image_{filenameNumber}'
    filenameNumber += 1
    image_data = binascii.b2a_base64(imageStream.getvalue()).decode()
    data = {'filename': filename, 'image_data': image_data}
    jsondata = json.dumps(data)
    print(jsondata)
    client.publish(cameraPublishTopic, jsondata)

# timedeltas for sensor logging and image capture
imageCaptureTimeDelta = timedelta(seconds=10)
lastImageCaptureTime = datetime.now()

captureImage()
print('logging started')
while True:
    if datetime.now() - lastImageCaptureTime >= imageCaptureTimeDelta:
        lastImageCaptureTime = datetime.now()
        captureImage()
