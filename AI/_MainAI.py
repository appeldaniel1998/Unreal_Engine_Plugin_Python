import time

from AI.DummyAlgoThread import DummyAlgoThread
from AI.GradeAI import GradeAI
from Core.Logger import LoggerThread
from Core.utils import *

if __name__ == '__main__':
    simParams: SimulationParams = loadSimParams()
    logger = LoggerThread()  # Create a logger thread
    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl
    initSimulation(simParams=simParams, publicDroneControl=publicDroneControl)  # Initialize the simulation

    # Create and start the Grade thread
    grade = GradeAI(publicDroneControl=publicDroneControl,
                    logger=logger,
                    simParams=simParams)
    grade.start()

    # Create and start the dummy algo thread
    dummyAlgoThread = DummyAlgoThread(publicDroneControl=publicDroneControl, logger=logger, gradeThread=grade)
    dummyAlgoThread.start()

    try:
        while True:
            # Perform periodic checks or log statuses
            if not dummyAlgoThread.is_alive():
                logger.info("Player control thread has stopped. Stopping all threads.")
                grade.stop()
                break
            if not grade.is_alive():
                logger.info("Grade thread has stopped. Stopping all threads.")
                dummyAlgoThread.stop()
                break

            time.sleep(1)  # Reduce CPU usage

    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt. Shutting down threads...")

    finally:
        # Ensure all threads are stopped
        if dummyAlgoThread.is_alive():
            dummyAlgoThread.stop()
        if grade.is_alive():
            grade.stop()

        # Now you can safely join since you've signaled them to stop
        dummyAlgoThread.join()
        grade.join()

        logger.info("All threads stopped cleanly.")
