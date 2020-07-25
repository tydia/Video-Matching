from preprocess.objectDetector import ObjectDetector
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
    objThemeResourceBase = resourceBase + "/" + "object_detection_result"
    modelpath =  modelPath = config["resourceBaseDir"] + "/object_detection_model" + "/yolo.h5"
    if not os.path.exists(objThemeResourceBase):
        os.mkdir(objThemeResourceBase)
    databaseReader = VideoDataBaseReader(dataBasePath)
    videoNames = databaseReader.getVideoNames()
    objDetect = ObjectDetector(modelpath)
    videoDict = {}
    for vn in videoNames:
        print("Working on video " + vn)
        videoPath = databaseReader.getVideoPath(vn)
        videoImgSeq = RGBImgSeqReader.readJPGvideo(videoPath, vn)
        firstDataDetect, firstDataKeyframeVis = objDetect.data_video_object_detection(videoImgSeq)

        objs = [i for i in firstDataDetect]
        print(objs)
        videoDict[vn] = objs

    fileOuputName = objThemeResourceBase + "/" + "videos" + ".json"
    with open(fileOuputName, "w") as f:
        json.dump(videoDict, f, indent=4)

