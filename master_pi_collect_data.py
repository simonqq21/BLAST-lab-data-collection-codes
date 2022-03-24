import time
from datetime import datetime, date, time, timedelta
from config import role, sitename, uname
from config import sensorLoggingDelay
from config import csvDir, csvfilename
from config import sensorPublishTopic, mqttIP, mqttPort
import pandas as pd
import paho.mqtt.client as mqtt
import json
from sensors import BME280init

'''
Python program to collect temperature, humidity, and pressure from the BME280 sensor
connected to the master Pi every 10 minutes

master pi data output
csv file containing datetime, temperature, humidity, and pressure
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

# bme280 init
try:
    bme280 = BME280init()
except:
    print("bme280 sensor error")

# get columns from file
columns = pd.read_csv(csvDir + csvfilename).columns.values
print(columns)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

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
client.loop_start()

temperature = 0
pressure = 0
humidity = 0
def logData():
    temperature, pressure, humidity = BME280Read(bme280)
    data = [[datetime.now().strftime('%m/%d/%Y %H:%M'), sitename, uname, temperature, pressure, humidity]]
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
    if datetime.now() - lastSensorLogTime >= sensorLoggingTimeDelta:
        lastSensorLogTime = datetime.now()
        logData()
