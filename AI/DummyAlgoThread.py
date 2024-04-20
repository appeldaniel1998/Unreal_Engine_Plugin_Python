import json
import threading
import time
from pathlib import Path
from typing import List

from Core.Coordinate import Coordinate
from Core.Logger import LoggerThread as Logger
from Core.PublicDroneControl import PublicDroneControl


def read_json_to_list_of_lists() -> List[Coordinate]:
    """
    Reads the graphPointsConfig.json file and returns a list of Coordinate objects.
    :return: List[Coordinate] - list of Coordinate objects representing the points to visit
    """
    current_script_path = Path(__file__).resolve()  # Get the path of the current script
    root_path = current_script_path.parent.parent  # Navigate to the root directory. Adjust the number of .parent based on your directory structure
    path = root_path / 'ConfigFiles' / "graphPointsConfig.json"  # Construct the full path to the configuration file
    with open(path, 'r') as file:
        data = json.load(file)

    list_of_lists = []  # Initialize an empty list to store the lists of floats

    # Iterate through the sorted keys to maintain order
    for key in sorted(data.keys(), key=int):  # Sorting keys as integers to ensure correct order
        list_of_lists.append(Coordinate(data[key][0], data[key][1], data[key][2]))

    return list_of_lists


class DummyAlgoThread(threading.Thread):
    def __init__(self, publicDroneControl: PublicDroneControl, logger: Logger):
        super().__init__()
        self.publicDroneControl = publicDroneControl
        self.logger = logger
        self.pointsToVisit = read_json_to_list_of_lists()

        self._stop_event = threading.Event()

    def stop(self):
        """
        Stops the thread.
        :return:
        """
        self._stop_event.set()

    def is_stopped(self):
        """
        Returns whether the thread is stopped.
        :return: bool
        """
        return self._stop_event.is_set()

    def run(self):
        """
        Dummy algorithm to move the drone to the points specified in the graphPointsConfig.json file.
        :return:
        """
        try:
            self.logger.info("Running dummy algorithm...")

            self.publicDroneControl.turnCameraXDegreesAtSpeed(degrees=30, speedMultiplier=60)
            for point in self.pointsToVisit:
                if self.is_stopped():
                    break

                self.logger.info(f"Moving to point: {point}")
                self.publicDroneControl.rotateDroneTowardsLocation(point.x, point.y, point.z)  # Rotate towards the point
                self.publicDroneControl.moveDroneToLocation(point.x, point.y, point.z, speed=5, turnWithMove=False)  # Move to the point

                time.sleep(0.01)  # small delay to prevent hogging the CPU
        except Exception as e:
            self.logger.error("Error in PlayerControlThread: " + str(e))
            self.stop()
            raise e
