from os import listdir
from os.path import join
import numpy as np
from utils.Int2RGB import *
import json

class VideoDescriptorLoader(object):

    def __init__(self, resourceBasePath):
        self.__resourceBathPath = resourceBasePath

    def loadColorPerFrame(self):
        resourceDir = self.__resourceBathPath + "/" + "color_theme_per_frame"
        resourceDict = {}
        print(resourceDir)
        for file in listdir(resourceDir):
            videoPath = join(resourceDir, file)
            videoName = file.split(".")[0]
            img_data = np.zeros((600, 5, 3)).astype(np.uint8)
            with open(videoPath, "r") as f:
                index = 0
                for line in f.readlines():
                    rgbArray = line.split()
                    curArray = []
                    for color in rgbArray:
                        r, g, b = getRGBfromI(int(color))
                        curArray.append([r, g, b])
                    img_data[index] = curArray
                    index += 1
            resourceDict[videoName] = img_data
        return resourceDict

    def loadColorPerVideo(self):
        resourceDir = self.__resourceBathPath + "/" + "color_theme_per_video"
        filePath = resourceDir + "/" + "videos.json"
        with open(filePath, "r") as json_file:
            tmpDict = json.load(json_file)
        resourceDict = {}
        for vn in tmpDict:
            curDict = {}
            rgbArray = tmpDict[vn]["palete"]
            curArray = []
            for color in rgbArray:
                r, g, b = getRGBfromI(int(color))
                curArray.append([r, g, b])
            curDict["palete"] = np.array(curArray)
            curDict["freq"] = np.array(tmpDict[vn]["freq"])
            resourceDict[vn] = curDict
        return resourceDict

    def loadObjectPerVideo(self):
        resourceDir = self.__resourceBathPath + "/" + "object_detection_result"
        filePath = resourceDir + "/" + "videos.json"
        with open(filePath, "r") as json_file:
            tmpDict = json.load(json_file)
        resourceDict = {}
        for vn in tmpDict:
            resourceDict[vn] = tmpDict[vn]
        return resourceDict

    def loadMotionPerVideo(self):
        resourceDir = self.__resourceBathPath + "/" + "motion_detection_per_video"
        filePath = resourceDir + "/" + "videos.json"
        with open(filePath, "r") as json_file:
            tmpDict = json.load(json_file)
        resourceDict = {}
        for vn in tmpDict:
            resourceDict[vn] = tmpDict[vn]
        return resourceDict

if __name__ == "__main__":
    videoDstor = VideoDescriptorLoader("/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/resource")
    # res = videoDstor.loadColorPerFrame()
    res = videoDstor.loadColorPerVideo()
    cur = res["flowers"]["palete"]
    print(cur)