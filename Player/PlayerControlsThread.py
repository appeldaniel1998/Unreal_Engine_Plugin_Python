import threading
import time

import keyboard

from Core.Logger import LoggerThread as Logger
from Core.PublicDroneControl import PublicDroneControl
from Player.GradePlayer import GradePlayer


class PlayerControlThread(threading.Thread):
    def __init__(self, publicDroneControl: PublicDroneControl, logger: Logger, gradeThread: GradePlayer):
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
            self.logger.info("Listening for keyboard input...")
            while not self._stop_event.is_set():
                if keyboard.is_pressed('w'):
                    self.publicDroneControl.moveDroneForward(1)
                    self.logger.info("Moving forward")
                if keyboard.is_pressed('s'):
                    self.publicDroneControl.moveDroneBackward(1)
                    self.logger.info("Moving backward")
                if keyboard.is_pressed('a'):
                    self.publicDroneControl.moveDroneLeft(1)
                    self.logger.info("Moving left")
                if keyboard.is_pressed('d'):
                    self.publicDroneControl.moveDroneRight(1)
                    self.logger.info("Moving right")
                if keyboard.is_pressed('r'):
                    self.publicDroneControl.rotateCameraUp(0.3)
                    self.logger.info("Rotating camera up")
                if keyboard.is_pressed('f'):
                    self.publicDroneControl.rotateCameraDown(0.3)
                    self.logger.info("Rotating camera down")
                if keyboard.is_pressed('q'):
                    self.publicDroneControl.rotateDroneLeft(0.3)
                    self.logger.info("Rotating drone left")
                if keyboard.is_pressed('e'):
                    self.publicDroneControl.rotateDroneRight(0.3)
                    self.logger.info("Rotating drone right")
                if keyboard.is_pressed('left shift'):
                    self.publicDroneControl.moveDroneUp(1)
                    self.logger.info("Moving up")
                if keyboard.is_pressed('left ctrl'):
                    self.publicDroneControl.moveDroneDown(1)
                    self.logger.info("Moving down")
                if keyboard.is_pressed('space'):
                    if self.publicDroneControl.verifyAndDestroyActorFromCamera():
                        self.logger.info("Actor detected by player, adding points... current points: " + str(self.gradePlayer.get_points()) + " + 1")
                        self.gradePlayer.add_points(1)
                    else:
                        self.logger.info("No actor detected by player")
                if keyboard.is_pressed('esc'):
                    self.logger.info("Stopping player control thread...")
                    self.stop()

                time.sleep(0.01)  # small delay to prevent hogging the CPU
        except Exception as e:
            self.logger.error("Error in PlayerControlThread: " + str(e))
            self.stop()
            raise e
