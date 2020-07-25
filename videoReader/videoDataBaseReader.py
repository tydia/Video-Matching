from os import listdir
from os.path import isdir, join

class VideoDataBaseReader(object):


    def __init__(self, dbDir):
        self.__baseDir = dbDir
        dirNames = []
        videoNames = []
        for dir in listdir(self.__baseDir):
            if isdir(join(self.__baseDir, dir)):
                dirNames.append(join(self.__baseDir, dir))
                videoNames.append(dir)
        self.__videoNames = set(videoNames)
        self.__name2dir = dict(zip(videoNames, dirNames))

    def getVideoNames(self):
        return [fileName for fileName in self.__videoNames]

    def getVideoPath(self, videoName):
        if not videoName in self.__videoNames:
            raise Exception("QueryVideo Name is not in the database")
        else:
            return self.__name2dir[videoName]

    def readVideo(self, videoName):
        dir = self.getVideoPath(videoName)

