import os
from pathlib import Path

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

loggingDuration = 300 # logging delay in sec, default 600secs for 10mins
datadir = Path.home() + '/blast_data/'

masterPiCSVFilename = "temperature_humidity_pressure_data.csv"
edgePiCSVFilename = "lightintensity_data.csv"
edgePiImagesDirectory = datadir + "images/"
edgePiImageFilenameFormat = "IMG_{datetime}_{uname}.jpg"

# create paths if they dont exist
create_path(datadir)
create_path(edgePiImagesDirectory)
