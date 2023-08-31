import time
import threading
import jparser
from jparser import gradeConfig
from jparser import setup_logger
from PublicDroneControl import PublicDroneControl
import keyboard
import Grade
import time
import threading
from Grade import Grade

if __name__ == '__main__':

    # Create a logger
    logger = setup_logger('my_log_file.log')

    # Create an instance of PublicDroneControl
    publicDroneControlObject = PublicDroneControl("127.0.0.1", 3001)

    # Initialize lastTime
    startTime = time.time()  # Store the initial time

    # Create and start the Grade thread
    grade_init = Grade(logger, publicDroneControlObject)

    # While the time of the simulation is not finished yet
    last_time = time.time()
    print("grade_init.simulationTime", grade_init.simulationTime)
    print("startTime", startTime)
    currTime = time.time()
    while currTime - startTime <= grade_init.simulationTime:
        # print("time.time()", time.time())

        if currTime - last_time > 1:
            # Decrease point each second
            grade_init.decrease_grade_each_sec()
            last_time = time.time()

        currTime = time.time()

        # Handle Points in case of collisions
        # pointsDecreaseCollision(grade_init)

        # decrease_grade_each_sec(grade_init)
        # time.sleep(1)
    grade_init.start()  # Starting the Grade thread

    #
    print("Program has finished.")

    # control the drone from the keyboard

    while True:
        if keyboard.is_pressed('w'):
            publicDroneControlObject.moveDroneForward(1)
        if keyboard.is_pressed('s'):
            publicDroneControlObject.moveDroneBackward(1)
        if keyboard.is_pressed('a'):
            publicDroneControlObject.moveDroneLeft(1)
        if keyboard.is_pressed('d'):
            publicDroneControlObject.moveDroneRight(1)
        if keyboard.is_pressed('q'):
            publicDroneControlObject.rotateDroneLeft(1)
        if keyboard.is_pressed('e'):
            publicDroneControlObject.rotateDroneRight(1)
        if keyboard.is_pressed('left shift'):
            publicDroneControlObject.moveDroneUp(1)
        if keyboard.is_pressed('left ctrl'):
            publicDroneControlObject.moveDroneDown(1)
        if keyboard.is_pressed('esc'):
            break
        time.sleep(0.01)  # small delay to prevent hogging the CPU
