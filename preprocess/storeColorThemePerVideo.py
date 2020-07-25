from preprocess.colorDescriptor import ColorDescriptor
from preprocess.rgbImgSeqReader import RGBImgSeqReader
from utils.Int2RGB import *
from videoReader.videoDataBaseReader import VideoDataBaseReader
import json
import os

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)
    dataBasePath = config["jpgDatabaseDir"]
    resourceBase = config["resourceBaseDir"]
    colorThemeResourceBase = resourceBase + "/" + "color_theme_per_video"
    if not os.path.exists(colorThemeResourceBase):
        os.mkdir(colorThemeResourceBase)
    databaseReader = VideoDataBaseReader(dataBasePath)
    videoNames = databaseReader.getVideoNames()

    videoDict = {}
    for vn in videoNames:
        print("Working on video " + vn)
        videoPath = databaseReader.getVideoPath(vn)
        videoLen = RGBImgSeqReader.getVideoFrameNum(videoPath)
        colorPalete, colorFreq = ColorDescriptor.getDataVideoColorDescriptor(videoPath, videoLen, vn)

        palete = [getIfromRGB(i) for i in colorPalete]
        freq = [i for i in colorFreq]
        videoDict[vn] = {"palete": palete, "freq": freq}

    fileOuputName = colorThemeResourceBase + "/" + "videos" + ".json"
    with open(fileOuputName, "w") as f:
        json.dump(videoDict, f, indent=4)

