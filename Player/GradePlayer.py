import threading
import time

from Core.DroneState import DroneState
from Core.Logger import LoggerThread as Logger
from Core.PublicDroneControl import PublicDroneControl
from Core.SimulationParams import SimulationParams


class GradePlayer(threading.Thread):
    def __init__(self, publicDroneControl: PublicDroneControl, logger: Logger, simParams: SimulationParams):
        super().__init__()

        self.publicDroneControl = publicDroneControl
        self.logger = logger
        self.simulationTime = simParams.simulationTime  # Duration in seconds
        self.addPointsForRecognition = simParams.addPointsForRecognition
        self.decreasePointsPerSec = simParams.decreasePointsPerSec
        self.pointsDeductedForCollision = simParams.pointsDeductedForCollision
        self.points = simParams.initialPoints  # Starting with a number of points

        self._stop_event = threading.Event()
        self._lock = threading.Lock()  # To ensure thread-safe operations

        # Utility variables
        self.simulation_start_time = time.time()
        self.last_point_time = time.time()

    def run(self):
        try:
            self.simulation_start_time = time.time()
            self.last_point_time = self.simulation_start_time
            current_time = time.time()

            while not self._stop_event.is_set() and (current_time - self.simulation_start_time) < self.simulationTime:  # Run for the duration of the simulation or until stopped
                current_time = time.time()
                self._handlePerSecondDeduction(current_time)
                self._handleCollisions()
                self.logger.info(f"Points: {self.points}")
                time.sleep(0.01)  # Sleep for a very short time to keep responsiveness high

        except Exception as e:
            self.logger.exception(f"Error in GradePlayer: {e}")
        finally:
            self.logger.info(f"Grade thread ended. Final points: {self.points}")
            self.stop()  # Stop the thread after the duration

    def add_points(self, numOfPointsToAdd):
        with self._lock:
            self.points += numOfPointsToAdd  # Safely add points

    def stop(self):
        self._stop_event.set()

    def get_points(self):
        return self.points

    def is_stopped(self):
        return self._stop_event.is_set()

    def _handlePerSecondDeduction(self, current_time: float) -> None:
        """
        Deducts a point every second
        :param current_time:  The current time in seconds
        """
        if current_time - self.last_point_time >= 1:  # Check if a full second has passed since the last point deduction
            with self._lock:
                self.points -= self.decreasePointsPerSec  # Deduct points
                self.last_point_time = current_time

    def _handleCollisions(self):
        """
        Function to handle the collision of the drone with physical objects
        :return: None
        """
        state: DroneState = self.publicDroneControl.getDroneState()
        if state is not None and state.collisionCount != 0:
            self.points -= self.pointsDeductedForCollision
            self.logger.info(f"Collision detected. Points deducted: {self.pointsDeductedForCollision}")
            self.stop()  # Stop the thread if a collision is detected and end simulation
