import threading
import time
import logging
from datetime import datetime
from pathlib import Path


class LoggerThread:
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self):
        """
        Constructor of logger thread
        """
        self._lock = threading.Lock()  # To ensure thread-safe operations

        # Constructing the path to the log file -->
        current_script_path = Path(__file__).resolve()  # Get the path of the current script
        root_path = current_script_path.parent.parent  # Navigate to the root directory. Adjust the number of .parent based on your directory structure
        fileName = 'log_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = root_path / 'logs' / fileName  # Construct the full path to the configuration file

        #  Initiating logger -->
        self.logger = logging.getLogger("ServerLogger")
        self.logger.setLevel(logging.DEBUG)  # Recording all levels of logs
        f_handler = logging.FileHandler(path, 'w', encoding="utf-8")  # Destination path and encoding
        logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Format of log
        f_handler.setFormatter(logFormat)
        self.logger.addHandler(f_handler)  # <--

        self.logger.info("Logging initiated")  # Logging

    def getLogger(self):
        """
        Simple getter method to allow logging from outside the class
        :return: logger
        """
        return self.logger

    def info(self, msg: str) -> None:
        """
        Method to log info to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.info(msg)
            print(msg)

    def debug(self, msg: str) -> None:
        """
        Method to log debug to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.debug(msg)
            print(msg)

    def warning(self, msg: str) -> None:
        """
        Method to log warning to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.warning(msg)
            print(msg)

    def error(self, msg: str) -> None:
        """
        Method to log error to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.error(msg)
            print(msg)

    def critical(self, msg: str) -> None:
        """
        Method to log critical to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.critical(msg)
            print(msg)

    def exception(self, msg: str) -> None:
        """
        Method to log exception to file
        :param msg: message to log
        :return:
        """
        with self._lock:
            self.logger.exception(msg)
            print(msg)
