from PyQt5 import QtCore
from PyQt5.QtGui import QImage
import time

class VideoLoadingManager(QtCore.QObject):
    imageChanged = QtCore.pyqtSignal((QImage, int))

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.index = 0
        self.running = False
        self.prevTime = time.time()

    def setVideoLoader(self, imgLoader):
        self.videoLoader = imgLoader

    def loadingImgs(self):
        while True:
            curTime = time.time()
            if self.running and self.index < self.videoLoader.getVideoLenth() and curTime > self.prevTime:
                img = self.videoLoader.getImgAt(self.index)
                self.imageChanged.emit(img, self.index)
                self.index += 1
                self.prevTime += (1000 / 30) / 1000

    def play(self):
        self.running = True
        self.prevTime = time.time()

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.index = 0

    def setFramePos(self, pos):
        self.index = pos

    def getVideoLength(self):
        return self.videoLoader.getVideoLenth()

    def getOneFrame(self, pos):
        return self.videoLoader.getImgAt(pos)

    def existVideo(self):
        return hasattr(self, 'videoLoader')