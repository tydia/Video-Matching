import numpy as np
from skimage import io
from os import mkdir
from os.path import exists
import shutil

from videoReader.videoDataBaseReader import VideoDataBaseReader

class Rgb2jpegConverter(object):

    def __init__(self, baseDir):
        self.__reader = VideoDataBaseReader(baseDir)
        self.__outputPathBase = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/database_videos_jpeg"

    def run(self):
        videoNames = self.__reader.getVideoNames()
        for vn in videoNames:
            inputPath = self.__reader.getVideoPath(vn)
            outputPath = self.__outputPathBase + "/" + vn
            self.convert(vn, inputPath, outputPath)
            self.copySound(vn, inputPath, outputPath)

    def convert(self, videoName, inputPath, outputPath):
        inputFileNames = []
        outputFileNames = []
        for i in range(1, 601, 1):
            if (i<10):
                fnStr = "00"+str(i)
            elif (i<100):
                fnStr = "0"+str(i)
            else:
                fnStr = str(i)
            finalInputFn = videoName + fnStr+".rgb"
            finalOutputFn = videoName + fnStr+".jpg"
            inputFileNames.append(finalInputFn)
            outputFileNames.append(finalOutputFn)
        #     print(finalOutputFn)
        for i in range(600):
            byte_list = []
            with open(inputPath + "/" + inputFileNames[i], "rb") as f:
                byte = f.read(1)
                while byte != b"":
                    # Do stuff with byte.
                    byte_list.append(byte)
                    byte = f.read(1)

            # image size: h*w*3=288*352*3. (Python's order is different from Java's)
            img_data = np.zeros((288,352,3)).astype(np.uint8)

            height = 288
            width = 352
            ind = 0
            for y in range(height):
                for x in range(width):
                    r=int.from_bytes(byte_list[ind], byteorder='big')
                    g=int.from_bytes(byte_list[ind+height*width], byteorder='big')
                    b=int.from_bytes(byte_list[ind+height*width*2], byteorder='big')

                    img_data[y][x][0] = r
                    img_data[y][x][1] = g
                    img_data[y][x][2] = b

                    ind+=1
            if not exists(outputPath):
                mkdir(outputPath)
            io.imsave(outputPath + "/" + outputFileNames[i], img_data)

    def copySound(self, videoName, inputPath, outputPath):
        print("Copying Sound for " + videoName)
        inputPath = inputPath + "/" + videoName + ".wav"
        outputPath = outputPath + "/" + videoName + ".wav"
        shutil.copyfile(inputPath, outputPath)

if __name__ == "__main__":
    rgbBase = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/database_videos"
    converter = Rgb2jpegConverter(rgbBase)
    converter.run()