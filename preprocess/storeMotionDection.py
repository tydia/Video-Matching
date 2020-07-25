import json
from preprocess.motionDescriptor import MotionDetector
from videoReader.videoDataBaseReader import VideoDataBaseReader
from preprocess.rgbImgSeqReader import RGBImgSeqReader
import os

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)
    dataBasePath = config["jpgDatabaseDir"]
    resourceBase = config["resourceBaseDir"]
    motionThemeResourceBase = resourceBase + "/" + "motion_detection_per_video"
    if not os.path.exists(motionThemeResourceBase):
        os.mkdir(motionThemeResourceBase)
    databaseReader = VideoDataBaseReader(dataBasePath)
    videoNames = databaseReader.getVideoNames()

    videoDict = {}
    for vn in videoNames:
        print("Working on video " + vn)
        videoPath = databaseReader.getVideoPath(vn)
        videoLen = RGBImgSeqReader.getVideoFrameNum(videoPath)
        imgs = RGBImgSeqReader.readJPGvideo(videoPath, vn)
        mDector = MotionDetector(imgs)
        mDector.run()
        fArray = mDector.getAvgMotions()
        videoDict[vn] = fArray

    fileOuputName = motionThemeResourceBase + "/" + "videos" + ".json"
    with open(fileOuputName, "w") as f:
        json.dump(videoDict, f, indent=4)

