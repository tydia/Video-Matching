from skimage import io
from qimage2ndarray import array2qimage
from os import listdir


class VideoReader(object):

    def __init__(self, videoPath):
        self.__images = []
        self.__videoName = videoPath.split('/')[-1]
        self.__videoPath = videoPath
        self.__videoLenth = self.__getVideoFrameNum()
        self.__audioPath = self.__videoPath + "/" + self.__videoName + ".wav"

    def loadImgs(self):
        image_list = []
        for i in range(1, self.__videoLenth + 1, 1):
            if i < 10:
                fnStr = "00" + str(i)
            elif i < 100:
                fnStr = "0" + str(i)
            else:
                fnStr = str(i)
            fileName = self.__videoPath + "/" + self.__videoName + fnStr + ".jpg"
            image_list.append(fileName)
        for f in image_list:
            img = io.imread(f)
            img = array2qimage(img)
            self.__images.append(img)

    def getVideoName(self):
        return self.__videoName

    def getImages(self):
        return self.__images

    def getImgAt(self, pos):
        return self.__images[pos]

    def getAudioPath(self):
        return self.__audioPath

    def getVideoPath(self):
        return self.__videoPath

    def getVideoLenth(self):
        return len(self.__images)

    def __getVideoFrameNum(self):
        fileList = listdir(self.__videoPath)
        if len(fileList) >= 600:
            return 600
        else:
            return 150

    def addVideoFrames(self, imgSeq):
        self.__images = []
        for f in imgSeq:
            img = array2qimage(f)
            self.__images.append(img)