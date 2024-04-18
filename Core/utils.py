import json
from pathlib import Path

from Core.PublicDroneControl import PublicDroneControl
from Core.SimulationParams import SimulationParams


def loadSimParams():
    # Constructing the path to the log file -->
    current_script_path = Path(__file__).resolve()  # Get the path of the current script
    root_path = current_script_path.parent.parent  # Navigate to the root directory. Adjust the number of .parent based on your directory structure
    path = root_path / 'ConfigFiles' / "gradeConfig.json"  # Construct the full path to the configuration file
    with open(path, "r") as file:  # Read info from file
        simulationParams: json = json.load(file)
    return SimulationParams(simulationParams["numOfPeople"], simulationParams["sunAngle"], simulationParams["addPointsForRecognition"],
                            simulationParams["decreasePointsPerSec"], simulationParams["simulationTime"], simulationParams["pointsDeductedForCollision"],
                            simulationParams["initialPoints"])


def initSimulation(simParams: SimulationParams, publicDroneControl: PublicDroneControl):
    publicDroneControl.spawnXActors(simParams.numOfPeople)  # Spawn actors
    publicDroneControl.requestDaytimeChange(simParams.sunAngle)  # Change sun angle
