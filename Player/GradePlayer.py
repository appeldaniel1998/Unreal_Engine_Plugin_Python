import threading
import time

from Core.DroneState import DroneState
from Core.Logger import LoggerThread as Logger
from Core.PublicDroneControl import PublicDroneControl


class GradePlayer(threading.Thread):
    def __init__(self, publicDroneControl: PublicDroneControl, logger: Logger, duration: float, pointsDeductedForCollision: int = 1000):
        super().__init__()
        self.logger = logger
        self.pointsDeductedForCollision = pointsDeductedForCollision
        self.publicDroneControl = publicDroneControl
        self.duration = duration  # Duration in seconds
        self.points = 0  # Start with 0 points
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

            while not self._stop_event.is_set() and (current_time - self.simulation_start_time) < self.duration:  # Run for the duration of the simulation or until stopped
                current_time = time.time()
                self._handlePerSecondDeduction(current_time)
                self._handleCollisions()
                print(f"Points: {self.points}")
                time.sleep(0.1)  # Sleep for a very short time to keep responsiveness high

            self.stop()  # Stop the thread after the duration
        except Exception as e:
            print(f"Error in GradePlayer: {e}")

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
                self.points -= 1
                self.last_point_time = current_time

    def _handleCollisions(self):
        state: DroneState = self.publicDroneControl.getDroneState()
        if state.collisionCount != 0:
            self.points -= self.pointsDeductedForCollision
            self.logger.info(f"Collision detected. Points deducted: {self.pointsDeductedForCollision}")
            self.stop()  # Stop the thread if a collision is detected and end simulation
