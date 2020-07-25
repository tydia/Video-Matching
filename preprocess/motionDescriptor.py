import numpy as np
import cv2
import json
from videoReader.videoDataBaseReader import VideoDataBaseReader
from preprocess.rgbImgSeqReader import RGBImgSeqReader
from numpy import dot
from numpy.linalg import norm

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

class MotionDetector(object):

    def __init__(self, video_seq):  # 构造方法，初始化一些参数和视频路径
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.images = video_seq
        self.frame_idx = 0
        self.avgMotion = []
        self.featureArray = []

    def run(self):

        for i in range(len(self.images)):
            frame = self.images[i]
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转化为灰度虚图像
            vis = frame.copy()

            if len(self.tracks) > 0:  # 检测到角点后进行光流跟踪
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None,
                                                       **lk_params)  # 前一帧的角点和当前帧的图像作为输入来得到角点在当前帧的位置
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None,
                                                        **lk_params)  # 当前帧跟踪到的角点及图像和前一帧的图像作为输入来找到前一帧的角点位置
                d = abs(p0 - p0r).reshape(-1, 2).max(-1)  # 得到角点回溯与前一帧实际角点的位置变化关系
                good = d < 1  # 判断d内的值是否小于1，大于1跟踪被认为是错误的跟踪点
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):  # 将跟踪正确的点列入成功跟踪点
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                tmpSum = 0
                for i in range(len(new_tracks)):
                    tmpSum += (new_tracks[i][0][0] - new_tracks[i][1][0]) **2 + \
                            (new_tracks[i][0][1] - new_tracks[i][1][1]) ** 2
                if len(new_tracks) is not 0:
                    self.avgMotion.append(tmpSum / len(new_tracks))
                else:
                    self.avgMotion.append(0)
                self.tracks = new_tracks
            if self.frame_idx % self.detect_interval == 0:  # 每5帧检测一次特征点
                mask = np.zeros_like(frame_gray)  # 初始化和视频大小相同的图像
                mask[:] = 255  # 将mask赋值255也就是算全部图像的角点
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:  # 跟踪的角点画圆
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)  # 像素级别角点检测
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])  # 将检测到的角点放在待跟踪序列中

            self.frame_idx += 1
            self.prev_gray = frame_gray
            self.calcBinaryDiff()

    def calcBinaryDiff(self):
        self.featureArray = []
        for i in range(1, len(self.avgMotion), 1):
            curDiff = self.avgMotion[i] - self.avgMotion[i - 1]
            if curDiff > 0:
                self.featureArray.append('1')
            else:
                self.featureArray.append('0')

    def getFeature(self):
        return self.featureArray

    def getAvgMotions(self):
        return self.avgMotion

    @staticmethod
    def compareBinaryDiff(queryStr, matchStr):
        # assuming len(matchStr) > len(queryStr)
        queryLen = len(queryStr)
        matchLen = len(matchStr)
        maxCounter = 0
        for i in range(queryLen):
            queryRest = queryStr[i::]
            for j in range(matchLen):
                counter = 0
                if j + len(queryRest) < matchLen:
                    for k in range(len(queryRest)):
                        if queryRest[k] == matchStr[j + k]:
                            counter += 1
                maxCounter = max(counter, maxCounter)
        return maxCounter / queryLen

    @staticmethod
    def compareCosineSim(queryDiffs, matchDiffs):
        queryLen = len(queryDiffs)
        matchLen = len(matchDiffs)
        maxSim = 0
        matchPosition = 0
        for i in range(matchLen):
            if i + queryLen < matchLen:
                tmpCosSin = dot(queryDiffs, matchDiffs[i:i + queryLen])/(norm(queryDiffs)*norm(matchDiffs[i:i + queryLen]))
                if tmpCosSin > maxSim:
                    maxSim = tmpCosSin
                    matchPosition = i
        return matchPosition, maxSim

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)
    videoReader = VideoDataBaseReader(config["jpgDatabaseDir"])
    videoName = "interview"
    videoPath = videoReader.getVideoPath(videoName)
    imgs = RGBImgSeqReader.readJPGvideo(videoPath, videoName)
    mDector = MotionDetector(imgs)
    mDector.run()

    fArray = mDector.getFeature()
    print("".join(fArray))