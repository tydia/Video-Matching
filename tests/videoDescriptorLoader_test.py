import unittest
from videoReader.videoDescriptorLoader import VideoDescriptorLoader
import json


class TestRGBImgSeqReader(unittest.TestCase):
    def setUp(self):
        with open('../config.json', 'r') as f:
            config = json.load(f)
        self.video = "flowers"
        self.__dataBasePath = config["resourceBaseDir"]
        self.videoDstor = VideoDescriptorLoader(self.__dataBasePath)

    def test_loadColorPerFrame(self):
        res = self.videoDstor.loadColorPerFrame()
        self.assertEqual(len(res), 7)
        self.assertEqual(res[self.video][14][0][0], 149)
        self.assertEqual(res[self.video][14][0][1], 151)
        self.assertEqual(res[self.video][14][0][2], 100)
        self.assertEqual(res[self.video][14][1][0], 104)
        self.assertEqual(res[self.video][14][4][0], 187)


    def test_readRGBVideos(self):
        print("Running second test: ")
        res = self.videoDstor.loadColorPerVideo()
        self.assertEqual(len(res), 7)