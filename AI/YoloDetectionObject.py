from typing import List


class YoloDetectionObject:
    """
    Class to represent the object detected by Yolo.
    """
    def __init__(self, asList: List):
        """
        :param asList:  input list of strings in the following format:
                        label, x_center, y_center, width, height, confidence
        """
        self.objectName = asList[0]
        self.xCenter = asList[1]
        self.yCenter = asList[2]
        self.width = asList[3]
        self.height = asList[4]
        self.confidence = asList[5]

    def __str__(self):
        return f"{self.objectName}"

    def __repr__(self):
        return self.__str__()
