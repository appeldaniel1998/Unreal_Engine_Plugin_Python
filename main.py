import json

from Logger import LoggerThread
from PublicDroneControl import PublicDroneControl
import keyboard
import time
from Grade import Grade
from datetime import datetime

if __name__ == '__main__':

    # Create a logger
    logger = LoggerThread("logs\\log_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))  # Create a logger thread

    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)  # Create an instance of PublicDroneControl

    # Initialize lastTime
    startTime = time.time()  # Store the initial time

    # Create and start the Grade thread
    grade = Grade(logger, publicDroneControl)
    grade.start()

    # Moving the drone on a graph --------------------------------------

    points = json.load(open("ConfigFiles/GraphPointsConfig.json", "r"))

    turn = True
    while True:
        if keyboard.is_pressed('q'):
            if turn:
                turn = False
            else:
                turn = True
        if keyboard.is_pressed('1'):
            publicDroneControl.moveDroneToLocation(points["0"][0], points["0"][1], points["0"][2], turnWithMove=turn)
        if keyboard.is_pressed('2'):
            publicDroneControl.moveDroneToLocation(points["1"][0], points["1"][1], points["1"][2], turnWithMove=turn)
        if keyboard.is_pressed('3'):
            publicDroneControl.moveDroneToLocation(points["2"][0], points["2"][1], points["2"][2], turnWithMove=turn)
        if keyboard.is_pressed('4'):
            publicDroneControl.moveDroneToLocation(points["3"][0], points["3"][1], points["3"][2], turnWithMove=turn)
        if keyboard.is_pressed('5'):
            publicDroneControl.moveDroneToLocation(points["4"][0], points["4"][1], points["4"][2], turnWithMove=turn)
        if keyboard.is_pressed('6'):
            publicDroneControl.moveDroneToLocation(points["5"][0], points["5"][1], points["5"][2], turnWithMove=turn)
        if keyboard.is_pressed('7'):
            publicDroneControl.moveDroneToLocation(points["6"][0], points["6"][1], points["6"][2], turnWithMove=turn)
        if keyboard.is_pressed('8'):
            publicDroneControl.moveDroneToLocation(points["7"][0], points["7"][1], points["7"][2], turnWithMove=turn)
        if keyboard.is_pressed('9'):
            publicDroneControl.moveDroneToLocation(points["8"][0], points["8"][1], points["8"][2], turnWithMove=turn)
    # -------------------------------------------------------------------

    # control the drone from the keyboard -------------------------------

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

    #  ----------------------------------------------------------------
