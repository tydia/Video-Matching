import sys
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QApplication, QScrollArea
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QImage, QPixmap
from videoReader.videoReader import VideoReader
from gui.VideoLoadingManager import VideoLoadingManager

class ImageShower(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__videoReader = VideoLoadingManager()
        lay = QGridLayout(self)
        gv = QGraphicsView()
        lay.addWidget(gv)
        scene = QGraphicsScene(self)
        gv.setScene(scene)
        gv.setContentsMargins(0, 0, 0, 0)
        self.pixmap_item = QGraphicsPixmapItem()
        self.player = QtMultimedia.QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.player.setPlaybackRate(0.925)
        scene.addItem(self.pixmap_item)
        gv.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.workerThread = QtCore.QThread()
        self.__videoReader.moveToThread(self.workerThread)
        self.workerThread.finished.connect(self.__videoReader.deleteLater)
        self.workerThread.started.connect(self.__videoReader.loadingImgs)
        self.__videoReader.imageChanged.connect(self.setImage)
        self.colorPaleteCallback = None
    def setupCallback(self, callback):
        self.callback = callback

    @QtCore.pyqtSlot(QImage, int)
    def setImage(self, image, index):
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item.setPixmap(pixmap)
        # position = self.player.position()
        # imgRate = (index / 600) * 100
        # audioRate = (position / 20010) * 100
        # print("{0:.2f}, {1:.2f}, position: {2:d}".format(imgRate, audioRate, position))

    def play(self):
        self.workerThread.start()
        self.__videoReader.play()
        self.player.play()

    def setupCallback(self, callback):
        self.colorPaleteCallback = callback

    def setupVideo(self, videoPath):
        videoReader = VideoReader(videoPath)
        videoReader.loadImgs()
        self.__videoReader.setVideoLoader(videoReader)
        print("video path: " + videoReader.getVideoPath())
        # setup audio
        fullPath = QtCore.QDir(videoReader.getVideoPath()).absoluteFilePath(videoReader.getVideoName() + ".wav")
        url = QtCore.QUrl.fromLocalFile(fullPath)
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        # self.player.setPlaybackRate(0.925)
        self.player.setMedia(content)
        self.stop()

    def setupVideoFromImgSeq(self, videoPath, imgSeq):
        videoReader = VideoReader(videoPath)
        videoReader.addVideoFrames(imgSeq)
        self.__videoReader.setVideoLoader(videoReader)
        print("video path: " + videoReader.getVideoPath())
        # setup audio
        fullPath = QtCore.QDir(videoReader.getVideoPath()).absoluteFilePath(videoReader.getVideoName() + ".wav")
        url = QtCore.QUrl.fromLocalFile(fullPath)
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        # self.player.setPlaybackRate(0.925)
        self.player.setMedia(content)
        self.stop()

    def setupVideoReader(self, videoReader):
        self.__videoReader.setVideoLoader(videoReader)
        fullPath = QtCore.QDir(videoReader.getVideoPath()).absoluteFilePath(videoReader.getVideoName() + ".wav")
        url = QtCore.QUrl.fromLocalFile(fullPath)
        content = QtMultimedia.QMediaContent(url)
        print("current video is: " + videoReader.getVideoName())
        self.player = QtMultimedia.QMediaPlayer()
        # self.player.setPlaybackRate(0.925)
        self.player.setMedia(content)
        self.stop()

    def pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.__videoReader.pause()
        else:
            self.player.play()
            self.__videoReader.play()

    def stop(self):
        self.player.stop()
        self.__videoReader.stop()
        self.workerThread.exit()

    def changeFrame(self, position):
        # It will never sync when you dragging the horizonalBar
        # print("current position is: {}".format(position))
        self.player.pause()
        self.__videoReader.pause()
        videoLen = self.__videoReader.getVideoLength()

        # self.player.setPosition(200 * position)
        # position = self.player.position()
        frameNum = int(6 * position)
        if self.colorPaleteCallback is not None:
            self.colorPaleteCallback(frameNum)
        pixmap = QPixmap.fromImage(self.fetchOneFrame(frameNum))
        self.pixmap_item.setPixmap(pixmap)
        self.__videoReader.setFramePos(frameNum)
        self.player.setPosition(200 * position)

    # def bindControl(self, bar):
    #     def changePositon(position):
    #         print("current position is: " + str(position))
    #     self.player.positionChanged.connect(changePositon)

    def fetchOneFrame(self, position):
        return self.__videoReader.getOneFrame(position)

    def existVideo(self):
        return self.__videoReader is not None and self.__videoReader.existVideo()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #scroll = QScrollArea()
    # scroll.setGeometry(QtCore.QRect(0, 0, 400, 300))

    w = ImageShower()
    w.setGeometry(QtCore.QRect(0, 0, 378, 314))
    w.show()
    w.setupVideo("/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/database_videos/traffic")
    w.play()
    sys.exit(app.exec_())