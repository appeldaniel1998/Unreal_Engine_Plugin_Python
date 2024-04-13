import time

from Core.Logger import LoggerThread
from Core.PublicDroneControl import PublicDroneControl
from Player.GradePlayer import GradePlayer
from Player.PlayerControlsThread import PlayerControlThread

if __name__ == '__main__':
    # grade = 0  # Start with 0 points

    logger = LoggerThread()  # Create a logger thread

    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl

    spawnedActors = publicDroneControl.spawnXActors(30)  # TODO change to getting from json
    # TODO get angle of sun from json

    # Create and start the Grade thread
    grade = GradePlayer(publicDroneControl, logger, 60)  # Duration in seconds
    grade.start()

    player_control_thread = PlayerControlThread(publicDroneControl=publicDroneControl, logger=logger)
    player_control_thread.start()

    try:
        while True:
            print("Main loop running...")
            # Perform periodic checks or log statuses
            if not player_control_thread.is_alive():
                print("Player control thread has stopped.")
                break
            if not grade.is_alive():
                print("Grade thread has stopped.")
                break

            time.sleep(1)  # Reduce CPU usage

    except KeyboardInterrupt:
        print("Shutting down threads...")
        # Signal all threads to stop, if you have implemented a stop mechanism.
        player_control_thread.stop()
        grade.stop()

        # Now you can safely join since you've signaled them to stop
        player_control_thread.join()
        grade.join()
        print("All threads stopped cleanly.")
