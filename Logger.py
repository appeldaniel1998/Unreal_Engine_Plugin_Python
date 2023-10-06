import threading
import time
import logging


class LoggerThread(threading.Thread):
    """
    A Thread class to handle the logging of the program to file
    """

    def __init__(self, name: str):
        """
        Constructor of logger thread
        :param name: Name of file to save to (without extension)
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        #  Initiating logger -->
        self.logger = logging.getLogger("ServerLogger")
        self.logger.setLevel(logging.DEBUG)  # Recording all levels of logs
        f_handler = logging.FileHandler(str(name) + '.log', 'w', encoding="utf-8")  # Destination path and encoding
        logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Format of log
        f_handler.setFormatter(logFormat)
        self.logger.addHandler(f_handler)  # <--

        self.logger.info("Logging initiated")  # Logging

    def stop(self):
        """
        Method to be called when the thread should be stopped
        :return:
        """
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        Method to be executed by the thread. Logs info from Airsim
        :return:
        """
        while not self.stopped():  # Thread stops upon call to stop() method above
            try:
                state = self.client.getMultirotorState()  # Get Airsim state data
                collision = self.client.simGetCollisionInfo()  # Get Airsim collision data
                self.logger.info("State:\n" + str(state))  # Logging
                self.logger.info("Collision:\n" + str(collision))  # Logging
                time.sleep(1)  # Log once per second
            except Exception as e:
                print(e)

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
        self.logger.info(msg)
        print(msg)

    def debug(self, msg: str) -> None:
        """
        Method to log debug to file
        :param msg: message to log
        :return:
        """
        self.logger.debug(msg)
        print(msg)

    def warning(self, msg: str) -> None:
        """
        Method to log warning to file
        :param msg: message to log
        :return:
        """
        self.logger.warning(msg)
        print(msg)

    def error(self, msg: str) -> None:
        """
        Method to log error to file
        :param msg: message to log
        :return:
        """
        self.logger.error(msg)
        print(msg)

    def critical(self, msg: str) -> None:
        """
        Method to log critical to file
        :param msg: message to log
        :return:
        """
        self.logger.critical(msg)
        print(msg)

    def exception(self, msg: str) -> None:
        """
        Method to log exception to file
        :param msg: message to log
        :return:
        """
        self.logger.exception(msg)
        print(msg)
