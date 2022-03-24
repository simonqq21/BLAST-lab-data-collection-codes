import os
from node_info import ROLE
from common import edgePiCollectData, masterPiCollectData


if ROLE == "master":
    masterPiCollectData()
else:
    edgePiCollectData()
