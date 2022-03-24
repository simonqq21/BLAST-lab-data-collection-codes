import os
import shutil
from config import homedir, datadir, edgePiImagesSubDir
from config import create_path

edgeDirFormat = "edge-pi{i}/"
destDir = 'images/'
create_path(destDir)
print(destDir)

os.system("rm -rf {cacheImagesPath}/*".format(cacheImagesPath = destDir))
n = 5
for i in range(1, n+1):
    currentEdgePiDir = homedir + edgeDirFormat.format(i=i) + edgePiImagesSubDir
    print(currentEdgePiDir)
    try:
        imageFilenames = os.listdir(currentEdgePiDir)
        imageFilenames.sort()
        latestImageFilename = imageFilenames[-1]
        print(currentEdgePiDir + latestImageFilename)
        print(destDir + latestImageFilename)
        shutil.copyfile(currentEdgePiDir + latestImageFilename, destDir + latestImageFilename)
        #os.system("cp {srcImagePath} {destImagePath}".format(srcImagePath=currentEdgePiDir + latestImageFilename, destImagePath = destDirComplete + latestImageFilename))
    except:
        pass
