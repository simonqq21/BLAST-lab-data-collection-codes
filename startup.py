import os
from node_info import ROLE
from common import edgePiCollectData, masterPiCollectData

if ROLE == "master":
    print("running master Pi program")
    masterPiCollectData()
else:
    print("running edge Pi program")
    edgePiCollectData()
