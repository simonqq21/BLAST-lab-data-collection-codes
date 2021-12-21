import os
from config import homedir, datadir, edgePiImagesSubDir

edgeDirFormat = "edge-pi{i}/"

n = 5
for i in range(1, n+1):
    currentEdgePiDir = homedir + edgeDirFormat.format(i=i) + edgePiImagesSubDir
    print(currentEdgePiDir)
    try:
        imageFilenames = os.listdir(currentEdgePiDir)
        imageFilenames.sort()
        latestImageFilename = imageFilenames[-1]
        os.system("cp {srcImagePath} {destImagePath}".format(srcImagePath=currentEdgePiDir + latestImageFilename, destImagePath = 'images'))
    except:
        pass
