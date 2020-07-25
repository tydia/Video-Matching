import unittest
from videoReader.videoDataBaseReader import VideoDataBaseReader

class TestVideoDataBaseReader(unittest.TestCase):

    def setUp(self):
        self.__dataBasePath = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/database_videos_jpeg"
        self.__queryVideo = "interview"
        self.__queryVideoPath = self.__dataBasePath + "/" + self.__queryVideo
        self.__reader = VideoDataBaseReader(self.__dataBasePath)

    def test_init(self):
        fileNames = self.__reader.getVideoNames()
        self.assertEqual(len(fileNames), 7)

    def test_get_video(self):
        dir = self.__reader.getVideoPath(self.__queryVideo)
        self.assertEqual(dir, self.__queryVideoPath)