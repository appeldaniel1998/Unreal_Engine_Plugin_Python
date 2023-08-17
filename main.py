import time

from publicDroneControl import PublicDroneControl
import keyboard

if __name__ == '__main__':
    publicDroneControl = PublicDroneControl("127.0.0.1", 3001)

    while True:
        if keyboard.is_pressed('w'):
            publicDroneControl.moveDroneForward(1)
        if keyboard.is_pressed('s'):
            publicDroneControl.moveDroneBackward(1)
        if keyboard.is_pressed('a'):
            publicDroneControl.moveDroneLeft(1)
        if keyboard.is_pressed('d'):
            publicDroneControl.moveDroneRight(1)
        if keyboard.is_pressed('q'):
            publicDroneControl.rotateDroneLeft(1)
        if keyboard.is_pressed('e'):
            publicDroneControl.rotateDroneRight(1)
        if keyboard.is_pressed('left shift'):
            publicDroneControl.moveDroneUp(1)
        if keyboard.is_pressed('left ctrl'):
            publicDroneControl.moveDroneDown(1)
        if keyboard.is_pressed('esc'):
            break
        time.sleep(0.01)  # small delay to prevent hogging the CPU
