import json
import threading
import time
from pathlib import Path

from Core import Logger
from AI.ArucoDetection import ArucoDetection
from Core.DroneState import DroneState
from Core.PublicDroneControl import PublicDroneControl
from Core.SimulationParams import SimulationParams
from YoloImpl.MainYoloDetect import YoloDetection
from AI.ThreadSafeResults import ThreadSafeResults


class GradeAI(threading.Thread):
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

    def __init__(self, logger: Logger.LoggerThread, publicDroneControl: PublicDroneControl, simParams: SimulationParams):
        """
        Constructor of the class. Reads the gradeConfig json file for the needed grading parameters.
        :param logger: logger to log the needed information
        :param publicDroneControl: PublicDroneControl object to access the needed information in run function
        :param simParams: SimulationParams object to get the needed parameters of the simulation
        """

        # Initializing the thread without running it
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()  # To ensure thread-safe operations

        self._publicDroneControl = publicDroneControl  # PublicDroneControl object to access the needed information in run function
        self._logger = logger  # Logger to file

        # Load parameters from JSON
        self._currentPoints: float = simParams.initialPoints  # Initial points
        self._simulationTime: float = simParams.simulationTime  # In seconds
        self._pointsForTargetDetection: float = simParams.addPointsForRecognition
        self._pointsDeductedPerCollision: float = simParams.pointsDeductedForCollision
        self._costPointsPerSec: float = simParams.decreasePointsPerSec

        # Object of thread, which when started will have the image analysis of Yolo of the current frame in video, which can be requested
        self._yoloResults = ThreadSafeResults()
        self._yoloDetectionThreadObj = YoloDetection(self._yoloResults)

        # Object of thread, which when started will analyze aruco codes of the current frame in video, which can be requested
        self._arucoResults = ThreadSafeResults()
        self._arucoDetectionThreadObj = ArucoDetection(self._arucoResults)

        # Util variables
        self.simulation_start_time = time.time()
        self.last_point_time = time.time()

    def stop(self):
        """
        Method to be called when the thread should be stopped (stop itself)
        :return: 
        """""
        self._yoloDetectionThreadObj.stop()
        self._arucoDetectionThreadObj.stop()
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
        try:
            self.simulation_start_time = time.time()
            self.last_point_time = self.simulation_start_time
            current_time = time.time()

            while not self._stop_event.is_set() and (current_time - self.simulation_start_time) < self._simulationTime:  # Run for the duration of the simulation or until stopped
                current_time = time.time()
                self._handleDecreaseGradeEachSec(current_time)
                self._handleCollision()
                self._handleImageFromUE()
                self._logger.info(f"Points: {self._currentPoints}")

                time.sleep(0.01)  # Sleep for a very short time to keep responsiveness high
        except Exception as e:
            self._logger.exception(f"Error in GradeAI: {e}")
        finally:
            self._logger.info(f"Grade thread ended. Final points: {self._currentPoints}")
            self.stop()  # Stop the thread after the duration

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

    def _handleDecreaseGradeEachSec(self, current_time: float):
        """
        Function decrease 1 point each second,
        To teach the drone that it depend on time.
        """
        if current_time - self.last_point_time >= 1:  # Check if a full second has passed since the last point deduction
            with self._lock:
                self._currentPoints -= self._costPointsPerSec  # Deduct points
                self.last_point_time = current_time

    def _handleCollision(self):
        """
        Function to handle the collision of the drone with physical objects
        :return: None
        """
        state: DroneState = self._publicDroneControl.getDroneState()
        if state is not None and state.collisionCount != 0:
            self._currentPoints -= self._pointsDeductedPerCollision
            self._logger.info(f"Collision detected. Points deducted: {self._pointsDeductedPerCollision}")
            self.stop()  # Stop the thread if a collision is detected and end simulation # Logging

    def _handleImageFromUE(self):
        if not self._yoloDetectionThreadObj.is_running():  # If the yolo thread is not yet running, run it
            self._yoloDetectionThreadObj.run()
        if not self._arucoDetectionThreadObj.is_running():  # If the aruco thread is not yet running, run it
            self._arucoDetectionThreadObj.run()

        yoloLatestResults = self._yoloResults.get_latest_results()  # get results of yolo detection (request results)
        self._logger.info("Yolo detection: " + str(yoloLatestResults))  # log results
        # TODO: add handling of seen objects. If not needed then remove previous 2 lines.

        arucoLatestResults = self._arucoResults.get_latest_results()  # get results of aruco codes detection (request results)
        self._logger.info("Yolo detection: " + str(arucoLatestResults))  # log results
        # TODO: add handling of seen aruco codes. If not needed then remove previous 2 lines.



