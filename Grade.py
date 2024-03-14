import json
import threading
import time

import Logger
from ArucoDetection import ArucoDetection
from PublicDroneControl import PublicDroneControl
from YoloImpl.MainYoloDetect import YoloDetection
from ThreadSafeResults import ThreadSafeResults


class Grade(threading.Thread):
    """
    Class to represent the thread which is to handle all grading-related issues of the drone for its Reinforcement Learning.
    Required functionality:
    1. Giving grade:
        1.1. Handle collisions of Drone with objects:
                For every collision, a certain number of points is deducted from the drone, according to the gradeConfig.json file.
        1.2. Handle time:
                For every second, a certain number of points is deducted from the drone, according to the gradeConfig.json file.
        1.3. Handle target recognition:
                Whenever a target is recognized (human or QR code), a certain number of points is added to the drone, according to the gradeConfig.json file.
    2. Sending the current grade at some rate per second to the client.
    """

    def __init__(self, logger: Logger.LoggerThread, publicDroneControl: PublicDroneControl):
        """
        Constructor of the class. Reads the gradeConfig json file for the needed grading parameters.
        :param logger: logger to log the needed information
        :param publicDroneControl: PublicDroneControl object to access the needed information in run function
        """

        # Initializing the thread without running it
        threading.Thread.__init__(self)
        self._publicDroneControl = publicDroneControl
        self._stop_event = threading.Event()

        self._logger = logger  # Logger to file

        gradeConfig = json.load(open("ConfigFiles/GradeConfig.json", "r"))  # Reading gradeConfig JSON from file
        # Load parameters from JSON
        self._currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        self._simulationTime: float = gradeConfig["simulationTime"]  # In seconds
        self._pointsForTargetDetection: float = gradeConfig["pointsForTargetDetection"]
        self._pointsDeductedPerCollision: float = gradeConfig["costPointsPerCollision"]
        self._costPointsPerSec: float = gradeConfig["costPointsPerSec"]

        # Object of thread, which when started will have the image analysis of Yolo of the current frame in video, which can be requested
        self._yoloResults = ThreadSafeResults()
        self._yoloDetectionThreadObj = YoloDetection(self._yoloResults)

        # Object of thread, which when started will analyze aruco codes of the current frame in video, which can be requested
        self._arucoResults = ThreadSafeResults()
        self._arucoDetectionThreadObj = ArucoDetection(self._arucoResults)

        # Util variables
        currTime = time.time()
        self._timeSinceLastSec = currTime

        self._timeSinceLastCollision = currTime
        self._lastCollisionCount = 0

    def stop(self):
        """
        Method to be called when the thread should be stopped (stop itself)
        :return: 
        """""
        self._yoloDetectionThreadObj.stop()
        self._stop_event.set()

    def stopped(self):
        """
        Check if the thread has been stopped
        :return:
        """
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread.
        :param self:
        :return:
        """
        startTime = time.time()  # Start time of the thread
        currTime = time.time()  # Current time of the thread

        while not self.stopped():  # Thread stops upon call to stop() method
            droneState = self._publicDroneControl.getDroneState()
            self._handleDecreaseGradeEachSec(currTime)
            self._handleEndSimulationTime(startTime, currTime)
            self._handleCollision(currTime, int(droneState["collisionCount"]))
            self._handleImageFromUE()
            currTime = time.time()  # Update current time

    def _handleEndSimulationTime(self, startTime: float, currTime: float):
        """
        Function to handle the end of the simulation time
        :param startTime: start time of the thread
        :param currTime: current time of the thread
        :return: None
        """
        if abs(currTime - startTime) > self._simulationTime:  # End of simulation time
            self._logger.info(f"Simulation has ended due to timeout. Final number of points: {self._currentPoints}")  # Logging
            self.stop()  # Stop thread

    def _handleDecreaseGradeEachSec(self, currTime: float):
        """
        Function decrease 1 point each second,
        To teach the drone that it depend on time.
        """
        if abs(currTime - self._timeSinceLastSec) > 1:  # Every second
            self._currentPoints -= self._costPointsPerSec
            self._timeSinceLastSec = currTime
            self._logger.info(f"Decrease points per sec: current points: {self._currentPoints} points")  # Logging

    def _handleCollision(self, currTime: float, collisionCount: int):
        """
        Function to handle the collision of the drone with physical objects
        :return: None
        """
        if collisionCount > self._lastCollisionCount:  # If collision occurred
            if currTime - self._timeSinceLastCollision > 2:  # if enough time passed since last collision (more than 2 seconds) (to avoid multiple collisions in a row)
                self._currentPoints -= self._pointsDeductedPerCollision
                self._timeSinceLastCollision = currTime
                self._lastCollisionCount = collisionCount
                self._logger.info(f"Collision Occurred! current points: {self._currentPoints} points")  # Logging

    def _handleImageFromUE(self):
        if not self._yoloDetectionThreadObj.is_running():  # If the yolo thread is not yet running, run it
            self._yoloDetectionThreadObj.run()
        if not self._arucoDetectionThreadObj.is_running():  # If the aruco thread is not yet running, run it
            self._arucoDetectionThreadObj.run()

        yoloLatestResults = self._yoloResults.get_latest_results()  # get results of yolo detection (request results)
        self._logger.info("Yolo detection: " + str(yoloLatestResults))  # log results
        # TODO: add handling of seen objects.

        arucoLatestResults = self._arucoResults.get_latest_results()  # get results of aruco codes detection (request results)
        self._logger.info("Yolo detection: " + str(arucoLatestResults))  # log results
        # TODO: add handling of seen aruco codes.



