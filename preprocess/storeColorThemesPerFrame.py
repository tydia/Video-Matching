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
    colorThemeResourceBase = resourceBase + "/" + "color_theme_per_frame"
    if not os.path.exists(colorThemeResourceBase):
        os.mkdir(colorThemeResourceBase)
    databaseReader = VideoDataBaseReader(dataBasePath)
    videoNames = databaseReader.getVideoNames()
    for vn in videoNames:
        print("Working on video " + vn)
        videoPath = databaseReader.getVideoPath(vn)
        videoLen = RGBImgSeqReader.getVideoFrameNum(videoPath)
        colorNp = ColorDescriptor.getFbyFColorDesc(videoPath, videoLen, vn)

        fileOuputName = colorThemeResourceBase + "/" + vn + ".txt"
        shape = colorNp.shape
        with open(fileOuputName, "w") as f:
            for i in range(shape[0]):
                curStr = ""
                for j in range(shape[1]):
                    rgb = getIfromRGB(colorNp[i][j])
                    curStr += str(rgb) + " "
                f.write(curStr + "\n")





