import cv2
import numpy as np
from preprocess.rgbImgSeqReader import RGBImgSeqReader
from preprocess.entropyChecker import EntropyChecker
from skimage import io
import json

class ColorDescriptor(object):

    @staticmethod
    def getFrameColorTheme(img):
        colorTheme = []
        n_colors_frame = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        # data for kmeans. each row is a pixel RGB value
        pixels = np.float32(img.reshape(-1, 3))

        # find 3 dominant colors with k-clustering
        _, labels, palette = cv2.kmeans(pixels, n_colors_frame, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)

        # indices reflect the importance of colors in palette based on how big is the value in counts
        indices = np.argsort(counts)[::-1]

        # append colors based on reordered indices
        for i in range(n_colors_frame):
            colorTheme.append(palette[indices[i]])

        # calculates frequency of each color in palette
        freqs = np.cumsum(np.hstack([[0], counts[indices] / counts.sum()]))

        return np.asarray(colorTheme), freqs

    # plt.imshow()
    @staticmethod
    def getDataVideoColorDescriptor(path_to_data_dir, num_files, fnString):
        # generate filenames for reading local images
        filenames = RGBImgSeqReader.generateFileNames(num_files, fnString, ".jpg")

        videoColorData = []
        for imgInd in range(num_files):
            currImg = io.imread(path_to_data_dir + "/" + filenames[imgInd])
            if (EntropyChecker.checkEntropy(currImg) == False):
                continue
            # if not first and last frame, check entropy difference
            if (imgInd != 0 and imgInd != num_files - 1):
                nextImg = io.imread(path_to_data_dir + "/" + filenames[imgInd + 1])
                if (EntropyChecker.checkInterframeEntropyDiff(nextImg, currImg) == False):
                    continue

            currImgTheme, currFreq = ColorDescriptor.getFrameColorTheme(currImg)
            videoColorData.append(currImgTheme)

        # reshape data so that it can be used by cv2.kmeans
        videoColorData = np.asarray(videoColorData)
        videoColorData = videoColorData.reshape(-1, 3)

        # do k-clustering again wrt videoColorData (complete video), pick 5 most dominant colors as color theme
        n_colors_video = 5
        # set epsilon to .01 so that it is more accurate when do kmeans on compele videos
        criteria_video = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .01)
        flags_video = cv2.KMEANS_RANDOM_CENTERS

        _, labels_video, palette_video = cv2.kmeans(videoColorData, n_colors_video, None, criteria_video, 10,
                                                    flags_video)
        _, counts_video = np.unique(labels_video, return_counts=True)
        # reorder colors based on counts
        indices_video = np.argsort(counts_video)[::-1]
        ordered_palette = np.zeros(shape=palette_video.shape, dtype=np.float32)
        for i in range(n_colors_video):
            ordered_palette[i] = palette_video[indices_video[i]]
        freqs_video = np.cumsum(np.hstack([[0], counts_video[indices_video] / counts_video.sum()]))
        return ordered_palette, freqs_video

    @staticmethod
    def getQueryVideoColorDescriptor(list_of_frames):
        videoColorData = []
        for imgInd in range(len(list_of_frames)):
            currImg = list_of_frames[imgInd]

            if (EntropyChecker.checkEntropy(currImg) == False):
                continue
            if (imgInd != 0 and imgInd != len(list_of_frames) - 1):
                nextImg = list_of_frames[imgInd + 1]
                if (EntropyChecker.checkInterframeEntropyDiff(nextImg, currImg) == False):
                    continue

            currImgTheme, currFreq = ColorDescriptor.getFrameColorTheme(currImg)
            videoColorData.append(currImgTheme)

        # reshape data so that it can be used by cv2.kmeans
        videoColorData = np.asarray(videoColorData)
        videoColorData = videoColorData.reshape(-1, 3)

        # do k-clustering again wrt videoColorData (complete video), pick 5 most dominant colors as color theme
        n_colors_video = 5
        # set epsilon to .01 so that it is more accurate when do kmeans on compele videos
        criteria_video = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .01)
        flags_video = cv2.KMEANS_RANDOM_CENTERS

        _, labels_video, palette_video = cv2.kmeans(videoColorData, n_colors_video, None, criteria_video, 10,
                                                    flags_video)
        _, counts_video = np.unique(labels_video, return_counts=True)
        # reorder colors based on counts
        indices_video = np.argsort(counts_video)[::-1]
        ordered_palette = np.zeros(shape=palette_video.shape, dtype=np.float32)
        for i in range(n_colors_video):
            ordered_palette[i] = palette_video[indices_video[i]]
        freqs_video = np.cumsum(np.hstack([[0], counts_video[indices_video] / counts_video.sum()]))
        return ordered_palette, freqs_video
    # pal, freq = getQueryVideoColorDescriptor(testimgList)

    @staticmethod
    def getFbyFColorDesc(path_to_data_dir, num_files, fnString):
        # generate filenames for reading local images
        colorThemes = []
        filenames = RGBImgSeqReader.generateFileNames(num_files, fnString, ".jpg")

        videoColorData = []
        for imgInd in range(num_files):
            currImg = io.imread(path_to_data_dir + "/" + filenames[imgInd])
            currImgTheme, _ = ColorDescriptor.getFrameColorTheme(currImg)
            colorThemes.append(currImgTheme)
        return np.asarray(colorThemes)

    @staticmethod
    def calcColorMatchScore(palette1, palette2, pal1freq):
        totalMatchScore = 0
        contribution = np.zeros(5)
        for i in range(5):
            contribution[i] = pal1freq[i+1]-pal1freq[i]
        for i in range(5):
            bestMatchScore = 0
            for j in range(5):
    #             currColorDist = colorMetric(palette1[i], palette2[j])
                currColorDist = EntropyChecker.colorMetricNorm(palette1[i], palette2[j])
                # calculate matching score
                currMatchScore = 1/(1+currColorDist)
                if (currMatchScore > bestMatchScore):
                    bestMatchScore = currMatchScore
            totalMatchScore += bestMatchScore *contribution[i]
        return np.around(totalMatchScore*100, decimals=2)

if __name__ == "__main__":

    numfiles = 150
    testDirPath = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/query/first"
    testFnString = "first"
    testPalette = ColorDescriptor.getFbyFColorDesc(testDirPath, numfiles, testFnString)
    print(testPalette[0][0])