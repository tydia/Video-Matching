from imageai.Detection import ObjectDetection
from skimage.color import rgb2gray
import numpy as np
from matplotlib import pyplot as plt
import cv2
from skimage.measure import shannon_entropy
import json
from preprocess.entropyChecker import EntropyChecker
from preprocess.rgbImgSeqReader import RGBImgSeqReader
class ObjectDetector(object):

    def __init__(self, modelPath):
        self.yoloDetector = ObjectDetection()
        self.yoloDetector.setModelTypeAsYOLOv3()
        self.yoloDetector.setModelPath(modelPath)
        self.yoloCustom = self.yoloDetector.CustomObjects(truck=False, bus=False, train=False, motorcycle=False,
                                                person=True, suitcase=True, tie=False, car=True,
                                                chair=True, couch=True, potted_plant=True, refrigerator=True,
                                                stop_sign=True, bench=True, bird=True, cat=True,
                                                dog=True, horse=True, sheep=True, cow=True,
                                                elephant=True, bear=True, zebra=True, giraffe=True,
                                                backpack=True, umbrella=True, handbag=True, frisbee=True,
                                                skis=True, snowboard=True, bottle=True, wine_glass=True,
                                                cup=True, fork=True, knife=True, spoon=True,
                                                bowl=True, banana=True, apple=True, sandwich=True,
                                                orange=True, broccoli=True, carrot=True, hot_dog=True,
                                                pizza=True, cake=True, bed=True, dining_table=True,
                                                toilet=True, tv=True, laptop=True, mouse=True,
                                                remote=True, keyboard=True, cell_phone=True, microwave=True,
                                                oven=True, toaster=True, sink=True, book=True,
                                                clock=True, vase=True, scissors=True, teddy_bear=True,
                                                hair_dryer=True, toothbrush=True, boat=True, traffic_light=True,
                                                fire_hydrant=True)
        self.yoloDetector.loadModel()

    @staticmethod
    def findKeyframes(list_of_frames):
        # calculate keyframes by getting F by F difference
        result = []
        for i in range(len(list_of_frames)):
            if (i == 0):
                prevImg = np.zeros((288, 352))
                currImg = rgb2gray(list_of_frames[i])
            else:
                prevImg = rgb2gray(list_of_frames[i])
                currImg = rgb2gray(list_of_frames[i - 1])
            # use the fact that 1-norm is the absolute difference. Fucking fast.
            frameDiff = cv2.norm(currImg, prevImg, cv2.NORM_L1)
            result.append(frameDiff)
        result = np.asarray(result)
        mean = np.mean(result)
        std = np.std(result)
        keyframes = np.argwhere(result > mean + std)
        keyframes = keyframes.reshape(-1, len(keyframes))[0]

        # clean up keyframes by entropy checking
        delete_ind = []
        for i in range(len(keyframes)):
            if (i == len(keyframes) - 1):
                break
            if (EntropyChecker.checkInterframeEntropyDiff(list_of_frames[keyframes[i]], list_of_frames[keyframes[i + 1]]) == False):
                delete_ind.append(i + 1)
        keyframes = np.delete(keyframes, delete_ind)
        return keyframes, result  # result is F by F diff differnce array, return this just for plot

    @staticmethod
    def checkInterframeEntropyDiff(img1, img2):
        entropyDiff = abs(shannon_entropy(img1) - shannon_entropy(img2))
        if (entropyDiff > 0.1):
            return True
        else:
            return False

    @staticmethod
    def plotFrameDiff1DArray(keyframes_1d_result):
        print("Frame difference analysis graph: ")
        plt.plot(keyframes_1d_result)
        plt.show()

    # detect objects from one image
    def img_object_detection(self, img):
        currRetImg, img_detections, extracted_objects = self.yoloDetector.detectCustomObjectsFromImage(
            custom_objects=self.yoloCustom,
            input_image=img,
            output_type="array",
            minimum_percentage_probability=55,
            input_type="array",
            display_percentage_probability=False,
            display_object_name=False,
            extract_detected_objects=True)
        img_detected_names = []
        for detectedObject in img_detections:
            img_detected_names.append(detectedObject["name"])
        objectName, _img_obj_counts = np.unique(img_detected_names, return_counts=True)
        return objectName


    # detect objects from a query video
    def query_video_object_detection(self, list_of_frames):
        keyframes, keyframes_visualization = self.findKeyframes(list_of_frames)
        #     print(keyframes)
        video_detected_obj_names = []
        for i in range(len(keyframes)):
            currKeyframe = list_of_frames[keyframes[i]]

            objectName = self.img_object_detection(currKeyframe)
            for name in objectName:
                if (name == 'tie'):
                    print(keyframes[i], "fuck")
                video_detected_obj_names.append(name)

        video_detected_obj_names, _ = np.unique(video_detected_obj_names, return_counts=True)
        return video_detected_obj_names, keyframes_visualization


    # detect objects from a data video
    def data_video_object_detection(self, list_of_frames):
        keyframes, keyframes_visualization = self.findKeyframes(list_of_frames)
        #     print(keyframes)
        video_detected_obj_names = []
        for i in range(len(keyframes)):
            currKeyframe = list_of_frames[keyframes[i]]

            objectName = self.img_object_detection(currKeyframe)
            for name in objectName:
                if (name == 'train'):
                    print(keyframes[i], "fuck")
                video_detected_obj_names.append(name)

            # also consider one frame prior to current keyframe as a keyframe
            if (keyframes[i] > 0):
                prevFrame = list_of_frames[keyframes[i] - 1]
                objectName2 = self.img_object_detection(prevFrame)
                for name in objectName2:
                    video_detected_obj_names.append(name)

        video_detected_obj_names, _ = np.unique(video_detected_obj_names, return_counts=True)
        return video_detected_obj_names, keyframes_visualization

    def calcObjDetMatchScore(queryObjArr, dataObjArr):
        common = set(queryObjArr).intersection(set(dataObjArr))
        match_score = len(common) / max(len(dataObjArr), len(queryObjArr))
        return np.around(match_score * 100, decimals=2)

if __name__ == "__main__":
    with open('../config.json', 'r') as f:
        config = json.load(f)
    modelPath = config["resourceBaseDir"] + "/object_detection_model" + "/yolo.h5"
    objDec = ObjectDetector(modelPath)
    testDirPath = "/Users/weiwang/Desktop/CSCI576/project/CSCI576-Final-Project/query/first"
    testFnString = "first"
    firstQuery = RGBImgSeqReader.readJPGvideo(testDirPath, testFnString)
    firstDataDetect, firstDataKeyframeVis = objDec.data_video_object_detection(firstQuery)
    print("flowers data detected objects", firstDataDetect)
