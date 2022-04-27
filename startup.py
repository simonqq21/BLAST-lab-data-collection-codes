import os
import pandas as pd
from node_info import ROLE
from common import create_path, edgePiCollectData, masterPiCollectData
from config import dataDir, csvDir, edgePiImgDir
from config import edgePiCSVFilename, masterPiCSVFilename

# create CSV file based on the role of the Pi
data=None
if ROLE == 'edge':
    data = {'role': [], 'datetime': [], 'sitename': [], 'hostname': [], 'lightintensity': []}
    csvfilename = edgePiCSVFilename

elif ROLE == 'master':
    data = {'role': [], 'datetime': [], 'sitename': [], 'hostname': [], 'temperature': [], \
        'pressure': [], 'humidity': []}
    csvfilename = masterPiCSVFilename

# run either master node data collection function or edge node data collection function
create_path(csvDir)
if data is not None:
    df = pd.DataFrame.from_dict(data, orient='columns')
    mode = 'w'
    index=False
    header=True
    if os.path.exists(csvDir + csvfilename):
        mode = 'a'
        header=False
        print('exists!')
    df.to_csv(csvDir + csvfilename, mode=mode, index=index, header=header)

if ROLE == "master":
    print("running master Pi program")
    masterPiCollectData()
else:
    print("running edge Pi program")
    create_path(edgePiImgDir)
    edgePiCollectData()
