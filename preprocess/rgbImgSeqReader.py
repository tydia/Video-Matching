import numpy as np
from os import listdir
import json
from skimage import io

class RGBImgSeqReader(object):

    @staticmethod
    def readRGBimg(path_to_file, filename):
        byte_list = []
        print("Loading File: " + filename)
        with open(path_to_file + "/" + filename, "rb") as f:
            byte = f.read(1)
            while byte != b"":
                byte_list.append(byte)
                byte = f.read(1)

        img_data = np.zeros((288, 352, 3)).astype(np.uint8)
        height = 288
        width = 352
        ind = 0
        for y in range(height):
            for x in range(width):
                a = 0
                r = int.from_bytes(byte_list[ind], byteorder='big')
                g = int.from_bytes(byte_list[ind + height * width], byteorder='big')
                b = int.from_bytes(byte_list[ind + height * width * 2], byteorder='big')

                img_data[y][x][0] = r
                img_data[y][x][1] = g
                img_data[y][x][2] = b

                ind += 1
        return img_data

    @staticmethod
    def generateFileNames(num_files, fnString, fileformat):
        retFileNames = []
        for i in range(1, num_files + 1, 1):
            if (i < 10):
                fnStr = "00" + str(i)
            elif (i < 100):
                fnStr = "0" + str(i)
            else:
                fnStr = str(i)
            currRetName = fnString + fnStr + fileformat
            retFileNames.append(currRetName)
        return retFileNames

    @staticmethod
    def readRGBvideo(path_to_file, fnString):
        retImgsList = []
        fileNum = RGBImgSeqReader.getVideoFrameNum(path_to_file)
        print("Number of files: " + str(fileNum))
        filenamesList = RGBImgSeqReader.generateFileNames(fileNum, fnString + "_", ".rgb")
        for i in range(fileNum):
            retImgsList.append(RGBImgSeqReader.readRGBimg(path_to_file, filenamesList[i]))
        return retImgsList

    @staticmethod
    def readJPGvideo(path_to_file, fnString):
        retImgsList = []
        fileNum = RGBImgSeqReader.getVideoFrameNum(path_to_file)
        print("Number of files: " + str(fileNum))
        filenamesList = RGBImgSeqReader.generateFileNames(fileNum, fnString, ".jpg")
        for i in range(fileNum):
            currImg = io.imread(path_to_file + "/" + filenamesList[i])
            retImgsList.append(currImg)
        return retImgsList

    @staticmethod
    def getVideoFrameNum(path_to_file):
        fileList = listdir(path_to_file)
        if len(fileList) >= 600:
            return 600
        else:
            return 150

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)

    dataBasePath = config["rgbDataBaseDir"]
    queryVideo = "interview"
    queryVideoPath = dataBasePath + "/" + queryVideo
    imgLists = RGBImgSeqReader.readRGBvideo(queryVideoPath, queryVideo)
