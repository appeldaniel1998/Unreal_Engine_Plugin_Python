import time

from Core.Logger import LoggerThread
from Core.PublicDroneControl import PublicDroneControl
from Player.GradePlayer import GradePlayer
from Player.PlayerControlsThread import PlayerControlThread

if __name__ == '__main__':

    logger = LoggerThread()  # Create a logger thread

    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl

    spawnedActors = publicDroneControl.spawnXActors(30)  # TODO change to getting from json
    # TODO get angle of sun from json

    # Create and start the Grade thread
    grade = GradePlayer(publicDroneControl, logger, 60)  # Duration in seconds
    grade.start()

    player_control_thread = PlayerControlThread(publicDroneControl=publicDroneControl, logger=logger, gradeThread=grade)
    player_control_thread.start()

    try:
        while True:
            # Perform periodic checks or log statuses
            if not player_control_thread.is_alive():
                logger.info("Player control thread has stopped unexpectedly. Stopping all threads.")
                grade.stop()
                break
            if not grade.is_alive():
                logger.info("Grade thread has stopped unexpectedly. Stopping all threads.")
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
