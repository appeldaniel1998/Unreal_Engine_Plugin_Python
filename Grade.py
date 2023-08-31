import json
import logging
import threading
import time

from PublicDroneControl import PublicDroneControl
from jparser import gradeConfig

import pymap3d as pm


# import numpy as np
# import cv2
# import geopy.distance
# import pymap3d as pm


class Grade(threading.Thread):
    """
    Class to represent the thread which is to handle all grading-related issues of the drone for its reinforcement learning.
    Current functionality:
    1. Giving grade:
        1.1. Handle collisions:
                Whenever the drone collides with a physical object, it is transported back to where it has been up to 10 seconds before (location updates every 10 seconds),
                one of its "lives" is removed, and some amount of points is deducted. These and other parameters are specified in the json file and from there the information is read.
        1.2. Handle recognising a Collision:
                Whenever a collision is recognised (from the image as the camera on the drone is seeing it), and is within a given radius from the drone,
                the number of points is taken away to the drone.
        1.3. Handle recognising a Human:
                Whenever a collision is recognised (from the image as the camera on the drone is seeing it), and is within a given radius from the drone,
                the number of points is awarded to the drone.
    2. Sending the current grade at some rate per second to the client.
    """

    def __init__(self, logger: logging.Logger, pdcObject: PublicDroneControl):
        """
        Constructor of the class. Reads the gradeConfig json file for the needed grading parameters.
        :param logger: logger to log the needed information
        :param pdcObject: PublicDroneControl object to access the needed information in run function
        :param clientCommunication: (will be implemented later)Tupple contains:socket for the final grade to be sent to via UDP,Address of the client for the grade to be sent to
        :param clientSocket:(will be implemented later) socket for the final grade to be sent to via UDP
        :param clientAddress:(will be implemented later) Address of the client for the grade to be sent to
        """
        # Initializing the thread without running
        threading.Thread.__init__(self)
        self.pdcObject = pdcObject
        self._stop_event = threading.Event()

        # Write all parameters to a log
        self.logger = logger  # Logger to file

        # Load parameters from JSON
        self.currentPoints: float = gradeConfig["pointsAtStartOfGame"]
        self.simulationTime: float = gradeConfig["simulationTime"]  # In seconds
        self.numOfCollisions: float = gradeConfig["CollisionCount"]  # int num
        self.costPerCollision: float = gradeConfig["collisionCost"]
        # self.droneRecognitionRadius: float = gradeConfig["droneRecognitionRadius"]  # Max radius from which the aruco codes are recognized by the drone
        # self.pointsForHumanDetected: float = gradeConfig["pointsForHumanDetected"]  # The number of points the agent receives upon detecting correctly a human

    def stop(self):
        """
        Method to be called when the thread should be stopped (stop itself)
        :return: 
        """""
        self._stop_event.set()

    def stopped(self):
        """
        Check if the thread has been stopped
        :return:
        """
        return self._stop_event.is_set()

    def decrease_grade_each_sec(self):
        """
        Function decrease 1 point each second,
        To teach the drone that it depend on time.
        """
        self.currentPoints -= 1
        print(f"current points: {self.currentPoints} points")

    def pointsDecreaseCollision(self):
        """
        FUNCTION NOT GOOD! NEED TO FIX!
        Function compute how many points decrease for all collisions
        :param self:
        :return:
        """
        pointsToDecrease = self.numOfCollisions * self.costPerCollision
        self.currentPoints = self.currentPoints - pointsToDecrease

        # self.numOfCollisions=0

    def run(self):
        """
        Method to be executed by the thread.
        :param self:
        :return:
        """
        # Start countdown and points decreasing
        # self.countdown_timer(self.simulationTime)
        # self.handleCollisions()  # Handle drone collisions

        # while True:
        #     #Get drone state
        #     PublicDroneControl.getDroneState(self.pdcObject)
        #
        #     #Decrease points because of collisions
        #     self.pointsDecreaseCollision()
