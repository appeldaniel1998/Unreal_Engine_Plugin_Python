import threading
import time

from AI.GradeAI import GradeAI
from Core.Logger import LoggerThread as Logger
from Core.PublicDroneControl import PublicDroneControl


class DummyAlgoThread(threading.Thread):
    def __init__(self, publicDroneControl: PublicDroneControl, logger: Logger, gradeThread: GradeAI):
        super().__init__()
        self.publicDroneControl = publicDroneControl
        self.logger = logger
        self.gradePlayer = gradeThread
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self):
        try:
            self.logger.info("Running dummy algorithm...")
            while not self._stop_event.is_set():
                time.sleep(0.01)  # small delay to prevent hogging the CPU
        except Exception as e:
            self.logger.error("Error in PlayerControlThread: " + str(e))
            self.stop()
            raise e
