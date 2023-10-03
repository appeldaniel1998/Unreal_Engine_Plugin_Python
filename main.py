from Logger import LoggerThread
from PublicDroneControl import PublicDroneControl
import keyboard
import time
from Grade import Grade

if __name__ == '__main__':

    # Create a logger
    logger = LoggerThread('my_log_file')

    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl

    # Initialize lastTime
    startTime = time.time()  # Store the initial time

    # Create and start the Grade thread
    grade_init = Grade(logger, publicDroneControl)
    grade_init.start()




    # control the drone from the keyboard

    # while True:
    #     if keyboard.is_pressed('w'):
    #         publicDroneControlObject.moveDroneForward(1)
    #     if keyboard.is_pressed('s'):
    #         publicDroneControlObject.moveDroneBackward(1)
    #     if keyboard.is_pressed('a'):
    #         publicDroneControlObject.moveDroneLeft(1)
    #     if keyboard.is_pressed('d'):
    #         publicDroneControlObject.moveDroneRight(1)
    #     if keyboard.is_pressed('q'):
    #         publicDroneControlObject.rotateDroneLeft(1)
    #     if keyboard.is_pressed('e'):
    #         publicDroneControlObject.rotateDroneRight(1)
    #     if keyboard.is_pressed('left shift'):
    #         publicDroneControlObject.moveDroneUp(1)
    #     if keyboard.is_pressed('left ctrl'):
    #         publicDroneControlObject.moveDroneDown(1)
    #     if keyboard.is_pressed('esc'):
    #         break
    #     time.sleep(0.01)  # small delay to prevent hogging the CPU
