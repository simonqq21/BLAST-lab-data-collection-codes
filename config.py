import os
from pathlib import Path
import pandas as pd

# create path if not exists
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# get environment variables for role ie. master or edge, hostname, and sitename
role = os.environ['ROLE']
sitename = os.environ['SITENAME']
uname = os.uname()[1]

loggingDuration = 5 # logging delay in sec, default 600secs for 10mins

# files and directories for collected data
datadir = str(Path.home()) + '/blast_data/'
masterPiCSVFilename = "temperature_humidity_pressure_data_{uname}_{sitename}.csv"
edgePiCSVFilename = "lightintensity_data_{uname}_{sitename}.csv"
edgePiImagesDirectory = datadir + "images/"
edgePiImageFilenameFormat = "IMG_{datetime}_{uname}_{sitename}.jpg"

# format the csv filenames
masterPiCSVFilename = masterPiCSVFilename.format(uname=uname, sitename=sitename)
edgePiCSVFilename = edgePiCSVFilename.format(uname=uname, sitename=sitename)
print(masterPiCSVFilename)
print(edgePiCSVFilename)

create_path(datadir)
create_path(edgePiImagesDirectory)

# create CSV file based on the role of the Pi
if role == 'edge':
    data = {'datetime': [], 'lightintensity': []}
    csvfilename = edgePiCSVFilename

elif role == 'master':
    data = {'datetime': [], 'temperature': [], 'pressure': [], 'humidity': []}
    csvfilename = masterPiCSVFilename

df = pd.DataFrame.from_dict(data, orient='columns')
mode = 'w'
index=False
header=True
if os.path.exists(csvfilename):
    mode = 'a'
    header=False
df.to_csv(datadir + csvfilename, mode=mode, index=index, header=header)
