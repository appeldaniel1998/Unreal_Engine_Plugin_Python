import time
import threading
import jparser
from jparser import y
from PublicDroneControl import PublicDroneControl
import keyboard

import time
import threading

def countdown_timer(seconds):
    while seconds > 0:
        print(f"Time left: {seconds} seconds")
        time.sleep(1)
        seconds -= 1
    print("Time's up!")
    global stop_threads
    stop_threads = True

def decrease_grade_each_sec(initial_grade, seconds):
    while seconds > 0 and not stop_threads:
        print(f"Grade at the end: {initial_grade} points")
        time.sleep(1)
        initial_grade -= 1

if __name__ == '__main__':
    stop_threads = False

    given_time = y["simulationTime"]
    initial_grade = y["initializedScore"]

    t1 = threading.Thread(target=countdown_timer, args=(given_time,))
    t2 = threading.Thread(target=decrease_grade_each_sec, args=(initial_grade, given_time))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Program has finished.")



    #control the drone from the keyboard
    publicDroneControlObject = PublicDroneControl("127.0.0.1", 3001)
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