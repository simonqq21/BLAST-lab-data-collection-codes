import os
import pandas as pd
from node_info import ROLE
from common import edgePiCollectData, masterPiCollectData
from config import edgePiCSVFilename, masterPiCSVFilename

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

# run either master node data collection function or edge node data collection function
if ROLE == "master":
    print("running master Pi program")
    masterPiCollectData()
else:
    print("running edge Pi program")
    edgePiCollectData()
