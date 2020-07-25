import json
from videoReader.videoDescriptorLoader import VideoDescriptorLoader
from preprocess.motionDescriptor import MotionDetector
from videoReader.videoDataBaseReader import VideoDataBaseReader
from preprocess.rgbImgSeqReader import RGBImgSeqReader
import os

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)
    dataBasePath = config["jpgDatabaseDir"]
    databaseReader = VideoDataBaseReader(dataBasePath)
    resourceBase = config["resourceBaseDir"]
    resourceloader = VideoDescriptorLoader(resourceBase)
    motionDict = resourceloader.loadMotionPerVideo()

    queryPath = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/query/first"
    queryName = "first"

    imgs = RGBImgSeqReader.readJPGvideo(queryPath, queryName)
    mDector = MotionDetector(imgs)
    mDector.run()
    fArray = mDector.getAvgMotions()
    for vn in databaseReader.getVideoNames():
        positon, score = MotionDetector.compareCosineSim(fArray, motionDict[vn])
        print("compare to {0}, score is {1:.2f}, matchPos is: {2}".format(vn, score, positon))
    # HQ1: starcraft: sports
    # HQ2: 速度激情: musicvideo
    # HQ4: flowers: musicvideo