import os
import pandas as pd

# create path if not exists
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# get environment variables for role ie. master or edge, hostname, and sitename
role = os.environ['ROLE']
sitename = os.environ['SITENAME']
uname = os.uname()[1]

sensorLoggingDelay = 600 # sensor logging delay in sec, default 600s for 10mins
imageCaptureDelay = 3600 # image capture delay in sec, default 3600s for 1hr

# files and directories for collected data
# homeDir = '/home/simonque/'
homeDir = '/home/pi/'
dataFolderName = 'blast_data/'
dataDir = homeDir + dataFolderName
csvFolderName = 'csv/'
imageFolderName = 'images/'
masterPiCSVFilename = "temperature_humidity_pressure_data_{uname}_{sitename}.csv"
edgePiCSVFilename = "lightintensity_data_{uname}_{sitename}.csv"
csvDir = dataDir + csvFolderName
edgePiImgDir = dataDir + imageFolderName
edgePiImageFilenameFormat = "IMG_{datetime}_{uname}_{sitename}.jpg"

# format the csv filenames
masterPiCSVFilename = masterPiCSVFilename.format(uname=uname, sitename=sitename)
edgePiCSVFilename = edgePiCSVFilename.format(uname=uname, sitename=sitename)
print(masterPiCSVFilename)
print(edgePiCSVFilename)

create_path(dataDir)
create_path(csvDir)
create_path(edgePiImgDir)

# create CSV file based on the role of the Pi
if role == 'edge':
    data = {'datetime': [], 'sitename': [], 'uname': [], 'lightintensity': []}
    csvfilename = edgePiCSVFilename

elif role == 'master':
    data = {'datetime': [], 'sitename': [], 'uname': [], 'temperature': [], \
        'pressure': [], 'humidity': []}
    csvfilename = masterPiCSVFilename

df = pd.DataFrame.from_dict(data, orient='columns')
mode = 'w'
index=False
header=True
if os.path.exists(dataDir + csvfilename):
    mode = 'a'
    header=False
df.to_csv(csvDir + csvfilename, mode=mode, index=index, header=header)

sensorPublishTopic = f"/shift/{sitename}/{uname}/sensorvalues"
cameraPublishTopic = f"/shift/{sitename}/{uname}/images"
mqttIP = "103.231.240.146"
mqttPort = 11000
