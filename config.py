import os
import pandas as pd
from node_info import SITENAME, HOSTNAME, ROLE

sensorLoggingDelay = 600 # sensor logging delay in sec, default 600s for 10mins
imageCaptureDelay = 3600 # image capture delay in sec, default 3600s for 1hr

'''
<homeDir>/<dataFolderName>/<{csvFolderName|imageFolderName}>/{masterPiCSVFilename|
edgePiCSVFilename|edgePiImageFilenameFormat}
'''
# files and directories for collected data
homeDir = '/home/pi/'
dataFolderName = 'blast_data/'
csvFolderName = 'csv/'
imageFolderName = 'images/'
masterPiCSVFilename = "temperature_humidity_pressure_data_{hostname}_{sitename}.csv"
edgePiCSVFilename = "lightintensity_data_{hostname}_{sitename}.csv"
edgePiImageFilenameFormat = "IMG_{datetime}_{hostname}_{sitename}.jpg"

dataDir = homeDir + dataFolderName
csvDir = dataDir + csvFolderName
edgePiImgDir = dataDir + imageFolderName

# format the csv filenames
masterPiCSVFilename = masterPiCSVFilename.format(hostname=HOSTNAME, sitename=SITENAME)
edgePiCSVFilename = edgePiCSVFilename.format(hostname=HOSTNAME, sitename=SITENAME)

if ROLE == 'edge':
    csvfilename = edgePiCSVFilename
elif ROLE == 'master':
    csvfilename = masterPiCSVFilename

sensorPublishTopic = f"/shift/{SITENAME}/{ROLE}/{HOSTNAME}/sensorvalues"
cameraPublishTopic = f"/shift/{SITENAME}/edge/{HOSTNAME}/images"
mqttIP = "ccscloud2.dlsu.edu.ph"
mqttPort = 20010
# mqttIP = "mqtt.eclipseprojects.io"
# mqttPort = 1883
