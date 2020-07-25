import unittest
from preprocess.rgbImgSeqReader import RGBImgSeqReader
import json

class TestRGBImgSeqReader(unittest.TestCase):
    def setUp(self):
        with open('../config.json', 'r') as f:
            config = json.load(f)

        self.__dataBasePath = config["rgbDataBaseDir"]
        self.__queryVideo = "interview"
        self.__queryVideoPath = self.__dataBasePath + "/" + self.__queryVideo

    def test_generateFileName(self):
        fileNames = RGBImgSeqReader.generateFileNames(100, self.__queryVideo, ".rgb")
        self.assertEqual(fileNames[0], "interview001.rgb")
        self.assertEqual(fileNames[9], "interview010.rgb")
        self.assertEqual(fileNames[99], "interview100.rgb")

    def test_readRGBVideos(self):
        print("Running second test: ")
        imgLists = RGBImgSeqReader.readRGBvideo(self.__queryVideoPath, self.__queryVideo)
        self.assertEqual(len(imgLists), 600)