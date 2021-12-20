import time
from adafruit_bme280 import basic as adafruit_bme280
import board
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import sensorLoggingDelay
from config import datadir, masterPiCSVFilename
import pandas as pd
import paho.mqtt.client as mqtt
import json

'''
Python program to collect temperature, humidity, and pressure from the BME280 sensor
connected to the master Pi every 10 minutes

master pi data output
csv file containing datetime, temperature, humidity, and pressure
mqtt publish with the data above

/shift/<sitename>/<hostname>/sensorvalues

/shift/dlsau/master-pi1/sensorvalues
/shift/dlsau/edge-pi1/sensorvalues
/shift/dlsau/edge-pi2/sensorvalues
/shift/dlsau/edge-pi3/sensorvalues
...

send json string of all sensor values
send image (WIP)
'''

# bme280 init
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

# get columns from file
columns = pd.read_csv(datadir + masterPiCSVFilename).columns.values
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
# publish_topic = f"/shift/DLSAU/master-pi/sensorvalues"
publish_topic = f"/shift/{sitename}/{uname}/sensorvalues"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# client.connect("103.231.240.146", 11000)
client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(client)
print(publish_topic)
client.loop_start()

temperature = 1
pressure = 2
humidity = 3
def logData():
    global temperature, pressure, humidity
    # temperature += 1
    # pressure += 2
    # humidity += 3
    temperature = bme280.temperature
    pressure = bme280.pressure
    humidity = bme280.relative_humidity
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), temperature, pressure, humidity]]
    print(data)
    df = pd.DataFrame(data, columns=columns)
    print(df)
    jsonData = df.to_json()
    client.publish(publish_topic, jsonData)
    df.to_csv(datadir+masterPiCSVFilename, mode='a', index=False, header=False)

# timedelta for sensor logging
sensorLoggingTimeDelta = timedelta(seconds=sensorLoggingDelay)
lastSensorLogTime = datetime.now()

logData()
print('logging started')
while True:
    if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
        lastSensorLogTime = datetime.now()
        logData()
