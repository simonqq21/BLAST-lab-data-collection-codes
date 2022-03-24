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

# create CSV file based on the role of the Pi
data=None
if ROLE == 'edge':
    data = {'datetime': [], 'sitename': [], 'hostname': [], 'lightintensity': []}
    csvfilename = edgePiCSVFilename

elif ROLE == 'master':
    data = {'datetime': [], 'sitename': [], 'hostname': [], 'temperature': [], \
        'pressure': [], 'humidity': []}
    csvfilename = masterPiCSVFilename

if data is not None:
    df = pd.DataFrame.from_dict(data, orient='columns')
    mode = 'w'
    index=False
    header=True
    if os.path.exists(dataDir + csvfilename):
        mode = 'a'
        header=False
    df.to_csv(csvDir + csvfilename, mode=mode, index=index, header=header)

    sensorPublishTopic = f"/shift/{SITENAME}/{HOSTNAME}/sensorvalues"
    cameraPublishTopic = f"/shift/{SITENAME}/{HOSTNAME}/images"

# mqttIP = "103.231.240.146"
# mqttPort = 11000
mqttIP = "mqtt.eclipseprojects.io"
mqttPort = 1883
