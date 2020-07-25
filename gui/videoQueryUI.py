# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videoQueryUIDesigin.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from videoReader.videoDataBaseReader import VideoDataBaseReader
from gui.imageShower import ImageShower
from gui.EmbedGraph import EmbedGraph
from videoReader.videoReader import VideoReader
from videoReader.videoDescriptorLoader import VideoDescriptorLoader
from preprocess.colorDescriptor import ColorDescriptor
from preprocess.entropyChecker import EntropyChecker
from preprocess.objectDetector import ObjectDetector
from preprocess.rgbImgSeqReader import RGBImgSeqReader
from preprocess.motionDescriptor import MotionDetector
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from os import listdir

class VideoQueryUI(object):

    def __init__(self, config):

        self.config = config
        self.dbReader = VideoDataBaseReader(config["jpgDatabaseDir"])
        self.path2VideoReader = {}
        self.resouceLoader = VideoDescriptorLoader(config["resourceBaseDir"])
        self.videoColorPerFrame = self.resouceLoader.loadColorPerFrame()
        self.videoColorPerVideo = self.resouceLoader.loadColorPerVideo()
        self.videoObjectPerVideo = self.resouceLoader.loadObjectPerVideo()
        self.videoMotionPerVideo = self.resouceLoader.loadMotionPerVideo()
        self.vn2ComparisonStat = {}
        modelPath = config["resourceBaseDir"] + "/object_detection_model" + "/yolo.h5"
        self.objDetect = ObjectDetector(modelPath)
        self.motionFeature = np.array([])
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 930)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.queryPlayer = ImageShower(self.centralwidget)
        self.queryPlayer.setGeometry(QtCore.QRect(90, 540, 378, 314))
        self.queryPlayer.setObjectName("queryVideoPane")

        self.matchPlayer = ImageShower(self.centralwidget)
        self.matchPlayer.setGeometry(QtCore.QRect(660, 540, 378, 314))
        self.matchPlayer.setObjectName("matchVideoPane")

        self.uploadQueryButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadQueryButton.setGeometry(QtCore.QRect(230, 90, 113, 32))
        self.uploadQueryButton.setObjectName("uploadQueryButton")
        self.uploadQueryButton.clicked.connect(self.uploadQueryVideo)

        self.uploadFileNameText = QtWidgets.QLineEdit(self.centralwidget)
        self.uploadFileNameText.setGeometry(QtCore.QRect(150, 60, 281, 21))
        self.uploadFileNameText.setObjectName("uploadFileNameText")

        self.aggregateResultText = QtWidgets.QLabel(self.centralwidget)
        self.aggregateResultText.setGeometry(QtCore.QRect(110, 160, 121, 16))
        self.aggregateResultText.setObjectName("uploadFileNameText")
        self.aggregateResultText.setText("Aggregate Result")

        self.aggregatePane = QtWidgets.QScrollArea(self.centralwidget)
        self.aggregatePane.setGeometry(QtCore.QRect(110, 180, 381, 141))
        self.aggregatePane.setFrameShape(QtWidgets.QFrame.Panel)
        self.aggregatePane.setWidgetResizable(True)
        self.aggregatePane.setObjectName("aggregatePane")
        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QVBoxLayout()

        for vn in self.dbReader.getVideoNames():
            videoPath = self.dbReader.getVideoPath(vn)
            print("Loading " + vn)
            group_box = QtWidgets.QGroupBox()
            layout = QtWidgets.QHBoxLayout(group_box)

            videoName = QtWidgets.QLabel()
            videoName.setText(vn)
            layout.addWidget(videoName)

            matchNum = QtWidgets.QLabel()
            matchNum.setText("0%")
            matchNum.setObjectName(vn + "_aggreg_result")
            layout.addWidget(matchNum)

            push_button = QtWidgets.QPushButton(group_box)
            push_button.setText('Choose')
            push_button.setFixedSize(100, 32)
            layout.addWidget(push_button)
            tmpVideoReader = VideoReader(videoPath)
            tmpVideoReader.loadImgs()
            self.path2VideoReader[videoPath] = tmpVideoReader
            push_button.clicked.connect(self.selectVideo(vn))
            self.top_layout.addWidget(group_box)

        self.top_widget.setLayout(self.top_layout)
        self.aggregatePane.setWidget(self.top_widget)

        self.colorDescriptoResult = QtWidgets.QScrollArea(self.centralwidget)
        self.colorDescriptoResult.setGeometry(QtCore.QRect(30, 360, 175, 151))
        self.colorDescriptoResult.setFrameShape(QtWidgets.QFrame.Panel)
        self.colorDescriptoResult.setWidgetResizable(True)
        self.colorDescriptoResult.setObjectName("colorDescriptoResult")
        self.colorDescriptoResult_top_widget = QtWidgets.QWidget()
        self.colorDescriptoResult_top_layout = QtWidgets.QVBoxLayout()

        self.colorDescriptorText = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorText.setGeometry(QtCore.QRect(30, 340, 121, 16))
        self.colorDescriptorText.setObjectName("colorDescriptorText")
        self.colorDescriptorText.setText("Color Descriptor")

        for vn in self.dbReader.getVideoNames():
            group_box = QtWidgets.QGroupBox()
            layout = QtWidgets.QHBoxLayout(group_box)

            videoName = QtWidgets.QLabel()
            videoName.setText(vn)
            layout.addWidget(videoName)

            matchNum = QtWidgets.QLabel()
            matchNum.setText("0%")
            matchNum.setObjectName(vn + "_aggreg_result")
            layout.addWidget(matchNum)
            self.colorDescriptoResult_top_layout.addWidget(group_box)

        self.colorDescriptoResult_top_widget.setLayout(self.colorDescriptoResult_top_layout)
        self.colorDescriptoResult.setWidget(self.colorDescriptoResult_top_widget)

        self.objectDescriptorResult = QtWidgets.QScrollArea(self.centralwidget)
        self.objectDescriptorResult.setGeometry(QtCore.QRect(210, 360, 175, 151))
        self.objectDescriptorResult.setFrameShape(QtWidgets.QFrame.Panel)
        self.objectDescriptorResult.setWidgetResizable(True)
        self.objectDescriptorResult.setObjectName("colorDescriptoResult")
        self.objectDescriptor_top_widget = QtWidgets.QWidget()
        self.objectDescriptor_top_layout = QtWidgets.QVBoxLayout()

        self.objectDescriptorText = QtWidgets.QLabel(self.centralwidget)
        self.objectDescriptorText.setGeometry(QtCore.QRect(210, 340, 121, 16))
        self.objectDescriptorText.setObjectName("objectDescriptorText")
        self.objectDescriptorText.setText("Object Descriptor")

        for vn in self.dbReader.getVideoNames():
            group_box = QtWidgets.QGroupBox()
            layout = QtWidgets.QHBoxLayout(group_box)

            videoName = QtWidgets.QLabel()
            videoName.setText(vn)
            layout.addWidget(videoName)

            matchNum = QtWidgets.QLabel()
            matchNum.setText("0%")
            matchNum.setObjectName(vn + "_aggreg_result")
            layout.addWidget(matchNum)
            self.objectDescriptor_top_layout.addWidget(group_box)

        self.objectDescriptor_top_widget.setLayout(self.objectDescriptor_top_layout)
        self.objectDescriptorResult.setWidget(self.objectDescriptor_top_widget)

        self.motionDescriptorResult = QtWidgets.QScrollArea(self.centralwidget)
        self.motionDescriptorResult.setGeometry(QtCore.QRect(390, 360, 175, 151))
        self.motionDescriptorResult.setFrameShape(QtWidgets.QFrame.Panel)
        self.motionDescriptorResult.setWidgetResizable(True)
        self.motionDescriptorResult.setObjectName("colorDescriptoResult")
        self.motionDescriptor_top_widget = QtWidgets.QWidget()
        self.motionDescriptor_top_layout = QtWidgets.QVBoxLayout()

        self.motionDescriptorText = QtWidgets.QLabel(self.centralwidget)
        self.motionDescriptorText.setGeometry(QtCore.QRect(390, 340, 121, 16))
        self.motionDescriptorText.setObjectName("uploadFileNameText")
        self.motionDescriptorText.setText("Motion Descriptor")

        for vn in self.dbReader.getVideoNames():
            group_box = QtWidgets.QGroupBox()
            layout = QtWidgets.QHBoxLayout(group_box)

            videoName = QtWidgets.QLabel()
            videoName.setText(vn)
            layout.addWidget(videoName)

            matchNum = QtWidgets.QLabel()
            matchNum.setText("0%")
            matchNum.setObjectName(vn + "_aggreg_result")
            layout.addWidget(matchNum)
            self.motionDescriptor_top_layout.addWidget(group_box)

        self.motionDescriptor_top_widget.setLayout(self.motionDescriptor_top_layout)
        self.motionDescriptorResult.setWidget(self.motionDescriptor_top_widget)

        self.colorDescriptorPaneText = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorPaneText.setGeometry(QtCore.QRect(670, 10, 121, 16))
        self.colorDescriptorPaneText.setObjectName("colorDescriptorPaneText")
        self.colorDescriptorPaneText.setText("Color Descriptor")

        self.colorDescriptorPaneText1 = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorPaneText1.setGeometry(QtCore.QRect(700, 40, 81, 16))
        self.colorDescriptorPaneText1.setObjectName("colorDescriptorPaneText1")
        self.colorDescriptorPaneText1.setText("Query Video")
        self.colorDescriptorPaneText2 = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorPaneText2.setGeometry(QtCore.QRect(810, 40, 81, 16))
        self.colorDescriptorPaneText2.setObjectName("colorDescriptorPaneText2")
        self.colorDescriptorPaneText2.setText("Match Video")
        self.colorDescriptorPaneText3 = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorPaneText3.setGeometry(QtCore.QRect(920, 40, 81, 16))
        self.colorDescriptorPaneText3.setObjectName("colorDescriptorPaneText3")
        self.colorDescriptorPaneText3.setText("Match Frame")

        self.colorDescriptorPaneWidget1 = QtWidgets.QGraphicsView(self.centralwidget)
        self.colorDescriptorPaneWidget1.setGeometry(QtCore.QRect(700, 70, 81, 80))
        self.colorDescriptorPaneWidget1.setObjectName("colorDescriptorPaneWidget1")
        self.colorDescriptorPaneWidget1Layout = QtWidgets.QVBoxLayout(self.colorDescriptorPaneWidget1)
        self.colorDescriptorPaneWidget1Layout.setContentsMargins(0, 0, 0, 0)
        self.colorDescriptorPaneWidget2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.colorDescriptorPaneWidget2.setGeometry(QtCore.QRect(810, 70, 81, 80))
        self.colorDescriptorPaneWidget2.setObjectName("colorDescriptorPaneWidget2")
        self.colorDescriptorPaneWidget2Layout = QtWidgets.QVBoxLayout(self.colorDescriptorPaneWidget2)
        self.colorDescriptorPaneWidget2Layout.setContentsMargins(0, 0, 0, 0)

        self.colorDescriptorPaneWidget3 = QtWidgets.QGraphicsView(self.centralwidget)
        self.colorDescriptorPaneWidget3.setGeometry(QtCore.QRect(920, 70, 81, 80))
        self.colorDescriptorPaneWidget3.setObjectName("colorDescriptorPaneWidget3")
        self.colorDescriptorPaneWidget3Layout = QtWidgets.QVBoxLayout(self.colorDescriptorPaneWidget3)
        self.colorDescriptorPaneWidget3Layout.setContentsMargins(0, 0, 0, 0)

        self.colorDescriptorPane = QtWidgets.QLabel(self.centralwidget)
        self.colorDescriptorPane.setGeometry(QtCore.QRect(670, 30, 351, 141))
        self.colorDescriptorPane.setFrameShape(QtWidgets.QFrame.Box)
        self.colorDescriptorPane.setObjectName("colorDescriptorPane")

        self.detectedObjectPaneText = QtWidgets.QLabel(self.centralwidget)
        self.detectedObjectPaneText.setGeometry(QtCore.QRect(670, 180, 121, 16))
        self.detectedObjectPaneText.setObjectName("detectedObjectPaneText")
        self.detectedObjectPaneText.setText("Detected Objects")

        self.detectedObjectPane = QtWidgets.QScrollArea(self.centralwidget)
        self.detectedObjectPane.setGeometry(QtCore.QRect(670, 200, 352, 141))
        self.detectedObjectPane.setWidgetResizable(True)
        self.detectedObjectPane.setObjectName("detectedObjectPane")
        self.detectedObjectPaneLayout = QtWidgets.QVBoxLayout(self.detectedObjectPane)
        self.detectedObjectPaneLayout.setContentsMargins(0, 0, 0, 0)

        self.motionMatchHeatGraphText = QtWidgets.QLabel(self.centralwidget)
        self.motionMatchHeatGraphText.setGeometry(QtCore.QRect(670, 350, 121, 16))
        self.motionMatchHeatGraphText.setObjectName("motionMatchHeatGraphText")
        self.motionMatchHeatGraphText.setText("Motion Descriptor")

        self.matchHeatGraph = QtWidgets.QScrollArea(self.centralwidget)
        self.matchHeatGraph.setGeometry(QtCore.QRect(670, 370, 352, 141))
        self.matchHeatGraph.setWidgetResizable(True)
        self.matchHeatGraph.setObjectName("matchHeatGraph")
        self.matchFigure = EmbedGraph(self.matchHeatGraph)
        self.matchFigure.setContentsMargins(0, 0, 0, 0)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(670, 520, 352, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalScrollBar.sliderMoved.connect(self.setPosition)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 845, 301, 32))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.queryVideoPlay = QtWidgets.QPushButton(self.widget)
        self.queryVideoPlay.setObjectName("queryVideoPlay")
        self.queryVideoPlay.clicked.connect(self.play(self.queryPlayer))

        self.horizontalLayout.addWidget(self.queryVideoPlay)
        self.queryVideoPause = QtWidgets.QPushButton(self.widget)
        self.queryVideoPause.setObjectName("queryVideoPause")
        self.queryVideoPause.clicked.connect(self.pause(self.queryPlayer))

        self.horizontalLayout.addWidget(self.queryVideoPause)
        self.queryVideoStop = QtWidgets.QPushButton(self.widget)
        self.queryVideoStop.setObjectName("queryVideoStop")
        self.queryVideoStop.clicked.connect(self.stop(self.queryPlayer))

        self.horizontalLayout.addWidget(self.queryVideoStop)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(695, 845, 301, 32))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.matchVideoPlay = QtWidgets.QPushButton(self.widget1)
        self.matchVideoPlay.setObjectName("matchVideoPlay")
        self.matchVideoPlay.clicked.connect(self.play(self.matchPlayer))
        self.horizontalLayout_2.addWidget(self.matchVideoPlay)

        self.matchVideoPause = QtWidgets.QPushButton(self.widget1)
        self.matchVideoPause.setObjectName("matchVideoPause")
        self.matchVideoPause.clicked.connect(self.pause(self.matchPlayer))
        self.horizontalLayout_2.addWidget(self.matchVideoPause)

        self.matchVideoStop = QtWidgets.QPushButton(self.widget1)
        self.matchVideoStop.setObjectName("matchVideoStop")
        self.matchVideoStop.clicked.connect(self.stop(self.matchPlayer))

        self.horizontalLayout_2.addWidget(self.matchVideoStop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.matchPlayer.bindControl(self.horizontalScrollBar)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.uploadQueryButton.setText(_translate("MainWindow", "upload query"))
        self.queryVideoPlay.setText(_translate("MainWindow", "Play"))
        self.queryVideoPause.setText(_translate("MainWindow", "Pause"))
        self.queryVideoStop.setText(_translate("MainWindow", "Stop"))
        self.matchVideoPlay.setText(_translate("MainWindow", "Play"))
        self.matchVideoPause.setText(_translate("MainWindow", "Pause"))
        self.matchVideoStop.setText(_translate("MainWindow", "Stop"))

    def setPosition(self, position):
        self.matchPlayer.setPosition(position)

    def uploadQueryVideo(self):
        wigdet = QtWidgets.QFileDialog()
        wigdet.setFileMode(QtWidgets.QFileDialog.Directory)
        wigdet.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        wigdet.setViewMode(QtWidgets.QFileDialog.Detail)
        directory = wigdet.getExistingDirectory(QtWidgets.QMainWindow(), 'Open Query Video Folder', QtCore.QDir.currentPath())
        if directory != '':
            fileType = self.getFileType(directory)
            print("The file type is: " + fileType)
            self.uploadFileNameText.setText(directory)
            # get video frames
            fileName = directory.split('/')[-1]
            if fileType == "jpg":
                queryFrames = RGBImgSeqReader.readJPGvideo(directory, fileName)
            else:
                queryFrames = RGBImgSeqReader.readRGBvideo(directory, fileName)
            # start the comparison between videos

            self.queryPlayer.setupVideoFromImgSeq(directory, queryFrames)
            colorPlatte, colorFreq = ColorDescriptor.getQueryVideoColorDescriptor(queryFrames)
            vn2ColorScore = {}
            colorScores = []
            for vn in self.dbReader.getVideoNames():
                targetColorPlate = self.videoColorPerVideo[vn]["palete"]
                # targetColorFreq = np.array(self.videoColorPerVideo[vn])
                score = ColorDescriptor.calcColorMatchScore(colorPlatte, targetColorPlate, colorFreq)
                colorScores.append(score)
                vn2ColorScore[vn] = score
            videoNames = self.dbReader.getVideoNames()
            video_names = [vn for _, vn in sorted(zip(colorScores, videoNames))]

            for vn in self.dbReader.getVideoNames():
                targetFrameColorPlates = self.videoColorPerFrame[vn]
                scoreList = []
                for i in range(targetFrameColorPlates.shape[0]):
                    score = ColorDescriptor.calcColorMatchScore(colorPlatte, targetFrameColorPlates[i], colorFreq)
                    scoreList.append(score)

            for i in range(self.colorDescriptoResult_top_layout.count()):
                self.colorDescriptoResult_top_layout.itemAt(i).widget().close()
            for vn in reversed(video_names):
                group_box = QtWidgets.QGroupBox()
                layout = QtWidgets.QHBoxLayout(group_box)

                videoName = QtWidgets.QLabel()
                videoName.setText(vn)
                layout.addWidget(videoName)

                matchNum = QtWidgets.QLabel()
                matchNum.setText(str(vn2ColorScore[vn]) + "%")
                layout.addWidget(matchNum)
                self.colorDescriptoResult_top_layout.addWidget(group_box)

            # compare object detection
            objResult, _ = self.objDetect.data_video_object_detection(queryFrames)
            print("Dection result: ")
            print(objResult)
            vn2ObjectScore = {}
            objectScores = []
            for vn in self.dbReader.getVideoNames():
                targetObjects = self.videoObjectPerVideo[vn]
                score = ObjectDetector.calcObjDetMatchScore(objResult, targetObjects)
                objectScores.append(score)
                vn2ObjectScore[vn] = score
            videoNames = self.dbReader.getVideoNames()
            video_names = [vn for _, vn in sorted(zip(objectScores, videoNames))]

            for i in range(self.objectDescriptor_top_layout.count()):
                self.objectDescriptor_top_layout.itemAt(i).widget().close()
            for vn in reversed(video_names):
                group_box = QtWidgets.QGroupBox()
                layout = QtWidgets.QHBoxLayout(group_box)

                videoName = QtWidgets.QLabel()
                videoName.setText(vn)
                layout.addWidget(videoName)

                matchNum = QtWidgets.QLabel()
                matchNum.setText(str(vn2ObjectScore[vn]) + "%")
                layout.addWidget(matchNum)
                self.objectDescriptor_top_layout.addWidget(group_box)

            # add detection result to Object Pane
            if self.detectedObjectPaneLayout.count() > 0:
                for i in range(self.detectedObjectPaneLayout.count() - 1, -1, -1):
                    self.detectedObjectPaneLayout.itemAt(i).widget().setParent(None)
            queryVideoBox = QtWidgets.QGroupBox()
            queryVideoBoxlayout = QtWidgets.QHBoxLayout(queryVideoBox)
            queryVideoBoxlayout.addWidget(QtWidgets.QLabel("Query Video Objects: "))
            for i in objResult:
                matchNum = QtWidgets.QLabel()
                matchNum.setText(i)
                queryVideoBoxlayout.addWidget(matchNum)
                self.detectedObjectPaneLayout.addWidget(queryVideoBox)

            # compare motion descriptor
            motionDescriptor = MotionDetector(queryFrames)
            motionDescriptor.run()
            queryMotionFeatures = motionDescriptor.getAvgMotions()
            self.motionFeature = queryMotionFeatures
            vn2MotionScore = {}
            motionScores = []
            for vn in self.dbReader.getVideoNames():
                targetFeature = self.videoMotionPerVideo[vn]
                pos, score = MotionDetector.compareCosineSim(queryMotionFeatures, targetFeature)
                motionScores.append(score * 100)
                self.vn2ComparisonStat[vn] = (pos, targetFeature)
                vn2MotionScore[vn] = np.around(score*100, decimals=2)
            videoNames = self.dbReader.getVideoNames()
            video_names = [vn for _, vn in sorted(zip(motionScores, videoNames))]

            for i in range(self.motionDescriptor_top_layout.count()):
                self.motionDescriptor_top_layout.itemAt(i).widget().close()
            for vn in reversed(video_names):
                group_box = QtWidgets.QGroupBox()
                layout = QtWidgets.QHBoxLayout(group_box)

                videoName = QtWidgets.QLabel()
                videoName.setText(vn)
                layout.addWidget(videoName)

                matchNum = QtWidgets.QLabel()
                matchNum.setText(str(vn2MotionScore[vn]) + "%")
                layout.addWidget(matchNum)
                self.motionDescriptor_top_layout.addWidget(group_box)


            # clear the original pane
            vn2TotalScore = {}
            totalScores = []
            for vn in self.dbReader.getVideoNames():
                score = vn2ColorScore[vn] * 0.5 + vn2ObjectScore[vn] * 0.2 + vn2MotionScore[vn] * 0.3
                totalScores.append(score)
                vn2TotalScore[vn] = np.around(score, decimals=2)
            videoNames = self.dbReader.getVideoNames()
            video_names = [vn for _, vn in sorted(zip(totalScores, videoNames))]
            for i in range(self.top_layout.count()):
                self.top_layout.itemAt(i).widget().close()
            # render aggregate pane
            for vn in reversed(video_names):
                group_box = QtWidgets.QGroupBox()
                layout = QtWidgets.QHBoxLayout(group_box)

                videoName = QtWidgets.QLabel()
                videoName.setText(vn)
                layout.addWidget(videoName)

                matchNum = QtWidgets.QLabel()
                matchNum.setText(str(vn2TotalScore[vn]) + "%")
                layout.addWidget(matchNum)

                push_button = QtWidgets.QPushButton(group_box)
                push_button.setText('Choose')
                push_button.setFixedSize(100, 32)
                layout.addWidget(push_button)
                push_button.clicked.connect(self.selectVideo(vn))
                self.top_layout.addWidget(group_box)
            # setup query video color palete image
            for i in range(self.colorDescriptorPaneWidget1Layout.count()):
                self.colorDescriptorPaneWidget1Layout.itemAt(i).widget().close()
            static_canvas = FigureCanvas(Figure())
            static_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
            self.colorDescriptorPaneWidget1Layout.addWidget(static_canvas)
            _static_ax = static_canvas.figure.subplots()
            curArray = EntropyChecker.showColorPalette(colorPlatte, colorFreq)
            _static_ax.imshow(curArray)
            _static_ax.axis('off')
            _static_ax.set_autoscale_on(True)
            static_canvas.show()

    def play(self, player):
        innerPlayer = player
        def innderPlay():
            innerPlayer.play()
        return innderPlay

    def pause(self, player):
        innerPlayer = player
        def innerPause():
            innerPlayer.pause()
        return innerPause

    def stop(self, player):
        innerPlayer = player
        def innerStop():
            innerPlayer.stop()
        return innerStop

    def selectVideo(self, vn):
        videoName = vn
        videoPath = self.dbReader.getVideoPath(vn)
        def selectMatchedVideo():
            # setup color palete
            for i in range(self.colorDescriptorPaneWidget2Layout.count()):
                self.colorDescriptorPaneWidget2Layout.itemAt(i).widget().close()
            static_canvas = FigureCanvas(Figure())
            static_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
            self.colorDescriptorPaneWidget2Layout.addWidget(static_canvas)
            _static_ax = static_canvas.figure.subplots()
            curArray = EntropyChecker.showColorPalette(self.videoColorPerVideo[videoName]["palete"],
                                                       self.videoColorPerVideo[videoName]["freq"])
            _static_ax.imshow(curArray)
            _static_ax.axis('off')
            _static_ax.set_autoscale_on(True)
            static_canvas.show()
            # setup match figure
            if videoName in self.vn2ComparisonStat:
                pos, targetVar = self.vn2ComparisonStat[videoName]
                self.matchFigure.addData(np.array(targetVar), pos, np.array(self.motionFeature))
            self.matchPlayer.setupCallback(self.generateCallback(videoName))
            self.matchPlayer.setupVideoReader(self.path2VideoReader[videoPath])
            # setup object
            if self.detectedObjectPaneLayout.count() > 1:
                num = self.detectedObjectPaneLayout.count()
                self.detectedObjectPaneLayout.itemAt(num - 1).widget().setParent(None)
            if self.detectedObjectPaneLayout.count() == 1:
                matchVideoBox = QtWidgets.QGroupBox()
                matchVideoBoxlayout = QtWidgets.QHBoxLayout(matchVideoBox)
                matchVideoBoxlayout.addWidget(QtWidgets.QLabel("Match Video Objects: "))
                for i in self.videoObjectPerVideo[videoName]:
                    matchNum = QtWidgets.QLabel()
                    matchNum.setText(i)
                    matchVideoBoxlayout.addWidget(matchNum)
                    self.detectedObjectPaneLayout.addWidget(matchVideoBox)
                self.detectedObjectPaneLayout.addWidget(matchVideoBox)
        return selectMatchedVideo

    def setPosition(self, position):
        if self.matchPlayer.existVideo():
            self.matchPlayer.changeFrame(position)

    def generateCallback(self, vn):
        videoName = vn
        framePalets = self.videoColorPerFrame[videoName]
        def callback(index):
            for i in range(self.colorDescriptorPaneWidget3Layout.count()):
                self.colorDescriptorPaneWidget3Layout.itemAt(i).widget().close()
            static_canvas = FigureCanvas(Figure())
            static_canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
            self.colorDescriptorPaneWidget3Layout.addWidget(static_canvas)
            _static_ax = static_canvas.figure.subplots()
            curArray = EntropyChecker.showColorPalette(framePalets[index],
                                                       np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
            _static_ax.imshow(curArray)
            _static_ax.axis('off')
            _static_ax.set_autoscale_on(True)
            static_canvas.show()
        return callback

    # def positionChanged(self, position):
    #     print("the position changed: " + position)
    #     self.horizontalScrollBar.setValue(position)
    def getFileType(self, directory):
        fileNames = listdir(directory)
        lastFileName = fileNames[-1]
        if lastFileName.split('.')[-1] == 'jpg':
            return "jpg"
        else:
            return "rgb"