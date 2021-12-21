import os
import shutil
from config import homedir, datadir, edgePiImagesSubDir, edgePiImagesDirectory
from config import create_path

edgeDirFormat = "edge-pi{i}/"
destDir = 'images/'
destDirComplete = os.getcwd() + '/' + destDir
create_path(edgePiImagesDirectory)
print(edgePiImagesDirectory)
#os.system("mkdir {destDirComplete}".format(destDirComplete=destDirComplete))

os.system("rm -rf {cacheImagesPath}".format(cacheImagesPath = edgePiImagesDirectory))
n = 5
for i in range(1, n+1):
    currentEdgePiDir = homedir + edgeDirFormat.format(i=i) + edgePiImagesSubDir
    print(currentEdgePiDir)
    try:
        imageFilenames = os.listdir(currentEdgePiDir)
        imageFilenames.sort()
        latestImageFilename = imageFilenames[-1]  
        print(currentEdgePiDir + latestImageFilename)
        print(destDirComplete + latestImageFilename)
        shutil.copyfile(currentEdgePiDir + latestImageFilename, edgePiImagesDirectory + latestImageFilename)
        #os.system("cp {srcImagePath} {destImagePath}".format(srcImagePath=currentEdgePiDir + latestImageFilename, destImagePath = destDirComplete + latestImageFilename))
    except:
        pass
