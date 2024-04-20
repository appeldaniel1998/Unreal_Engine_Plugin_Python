from typing import List


class YoloDetectionObject:
    def __init__(self, asList: List):
        self.objectName = asList[0]
        self.confidence = asList[1]
        self.xCenter = asList[2]
        self.yCenter = asList[3]
        self.width = asList[4]
        self.height = asList[5]
        # self.boundingBox = [asList[2], asList[3], asList[4], asList[5]]

    def __str__(self):
        return f"YoloDetectionObject: {self.objectName} at ({self.xCenter}, {self.yCenter}) with confidence {self.confidence}"

    def __repr__(self):
        return self.__str__()
