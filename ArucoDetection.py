import threading
import cv2
from cv2 import aruco

from ThreadSafeResults import ThreadSafeResults


class ArucoDetection(threading.Thread):
    def __init__(self, latest_results: ThreadSafeResults):
        # Initializing the thread without running it
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._start_event = threading.Event()  # Event to track if the thread has started
        self.latest_results: ThreadSafeResults = latest_results

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

    def has_started(self):
        """
        Check if the thread has been started.
        """
        return self._start_event.is_set()

    def is_running(self):
        """
        More explicit method to check if the thread is currently running.
        """
        return self.is_alive() and not self.stopped()

    def run(self):
        """
        Method to be executed by the thread.
        :param self:
        :return:
        """
        self._start_event.set()

        cap = cv2.VideoCapture(0)  # Initialize the webcam (0 is the default webcam)

        # Set the resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not cap.isOpened():  # Check if the webcam is opened correctly
            raise IOError("Cannot open webcam")

        while not self.stopped():
            ret, frame = cap.read()  # Read a frame
            if ret:  # Check if the frame is read correctly

                # Set up the Aruco dictionary and parameters
                arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
                arucoParams = aruco.DetectorParameters()

                corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)  # Detect aruco codes in frame
                self.latest_results.update_results((corners, ids, rejected))

            else:
                print("Aruco: Failed to capture frame")

        # Release the VideoCapture object
        cap.release()
