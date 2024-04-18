import json
import time
from pathlib import Path

from Core.Logger import LoggerThread
from Core.PublicDroneControl import PublicDroneControl
from Core.SimulationParams import SimulationParams
from Player.GradePlayer import GradePlayer
from Player.PlayerControlsThread import PlayerControlThread


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


def initSimulation():
    global publicDroneControl

    publicDroneControl.spawnXActors(simParams.numOfPeople)  # Spawn actors
    publicDroneControl.requestDaytimeChange(simParams.sunAngle)  # Change sun angle


if __name__ == '__main__':
    simParams: SimulationParams = loadSimParams()
    logger = LoggerThread()  # Create a logger thread
    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl
    initSimulation()  # Initialize the simulation

    # Create and start the Grade thread
    grade = GradePlayer(publicDroneControl=publicDroneControl,
                        logger=logger,
                        simulationTime=simParams.simulationTime,  # Duration in seconds
                        addPointsForRecognition=simParams.addPointsForRecognition,
                        decreasePointsPerSec=simParams.decreasePointsPerSec,
                        pointsDeductedForCollision=simParams.pointsDeductedForCollision,
                        initialPoints=simParams.initialPoints)
    grade.start()

    player_control_thread = PlayerControlThread(publicDroneControl=publicDroneControl, logger=logger, gradeThread=grade)
    player_control_thread.start()

    try:
        while True:
            # Perform periodic checks or log statuses
            if not player_control_thread.is_alive():
                logger.info("Player control thread has stopped. Stopping all threads.")
                grade.stop()
                break
            if not grade.is_alive():
                logger.info("Grade thread has stopped. Stopping all threads.")
                player_control_thread.stop()
                break

            time.sleep(1)  # Reduce CPU usage

    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt. Shutting down threads...")

    finally:
        # Ensure all threads are stopped
        if player_control_thread.is_alive():
            player_control_thread.stop()
        if grade.is_alive():
            grade.stop()

        # Now you can safely join since you've signaled them to stop
        player_control_thread.join()
        grade.join()

        logger.info("All threads stopped cleanly.")
