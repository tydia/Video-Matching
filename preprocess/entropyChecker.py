from skimage.measure import shannon_entropy
import numpy as np
import matplotlib.pyplot as plt

class EntropyChecker(object):

    @staticmethod
    def checkEntropy(inputImg):
        entropy = shannon_entropy(inputImg)
        if (entropy > 0.1):
            return True
        else:
            return False

    @staticmethod
    def checkInterframeEntropyDiff(img1, img2):
        entropyDiff = abs(shannon_entropy(img1) - shannon_entropy(img2))
        if (entropyDiff > 0.03):
            return True
        else:
            return False

    @staticmethod
    def colorMetric(c1, c2):
        rmean = (c1[0] + c2[0]) / 2
        dr = c1[0] - c2[0]
        dg = c1[1] - c2[1]
        db = c1[2] - c2[2]
        dist = np.sqrt((2 + rmean / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rmean) / 256) * db * db)
        # 765 is distance btwn white and black calculated use this metric.
        return dist / 765

    # normalized color distance to range 0 - 1.
    @staticmethod
    def colorMetricNorm(c1, c2):
        rmean = (c1[0] + c2[0]) / 2 / 256
        dr = (c1[0] - c2[0]) / 256
        dg = (c1[1] - c2[1]) / 256
        db = (c1[2] - c2[2]) / 256
        dist = np.sqrt((2 + rmean) * dr * dr + 4 * dg * dg + (2 + (1 - rmean)) * db * db)
        # 765 is distance btwn white and black calculated use this metric.
        return dist

    # show || save a color palette
    # 576 = 288*2 = height*2 removes artifacts at bottom of image
    @staticmethod
    def showColorPalette(palette, freq):
        rows = np.int_(576 * freq)
        dom_patch = np.zeros(shape=(576, 576, 3), dtype=np.uint8)
        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[i])
        return dom_patch

    @staticmethod
    def saveColorPalette(palette, freq, filename):
        rows = np.int_(576 * freq)
        dom_patch = np.zeros(shape=(576, 576, 3), dtype=np.uint8)
        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[i])
        plt.figure(figsize=(1, 1), dpi=100)
        plt.imshow(dom_patch)
        plt.axis('off')
        plt.savefig(filename, transparent=True)
        plt.show()