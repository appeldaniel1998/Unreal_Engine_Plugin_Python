import socket
import time
# from jparser import y


class PublicDroneControl:
    def __init__(self, ip, port):
        ip_portRecv = (ip, port)
        self.udp_socketRecv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # receiver socket (UDP) opened
        self.udp_socketRecv.bind(ip_portRecv)

        self.udp_socketSend = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # sender socket (UDP) opened
        self.ip_portSend = (ip, port + 1)

    def send(self, msg):
        self.udp_socketSend.sendto(msg.encode('utf-8'), self.ip_portSend)  # Send message to UE

    def moveDroneUp(self, multiplier):
        msg = '{"primitiveControls": {"upAmount": ' + str(multiplier) + '}}'
        self.send(msg)

    def moveDroneDown(self, multiplier):
        msg = '{"primitiveControls": {"upAmount": ' + str(-multiplier) + '}}'
        self.send(msg)

    def moveDroneForward(self, multiplier):
        msg = '{"primitiveControls": {"pitchForwardAmount": ' + str(multiplier) + '}}'
        self.send(msg)

    def moveDroneBackward(self, multiplier):
        msg = '{"primitiveControls": {"pitchForwardAmount": ' + str(-multiplier) + '}}'
        self.send(msg)

    def moveDroneRight(self, multiplier):
        msg = '{"primitiveControls": {"rollRightAmount": ' + str(multiplier) + '}}'
        self.send(msg)

    def moveDroneLeft(self, multiplier):
        msg = '{"primitiveControls": {"rollRightAmount": ' + str(-multiplier) + '}}'
        self.send(msg)

    def rotateDroneRight(self, multiplier):
        msg = '{"primitiveControls": {"yawRightAmount": ' + str(multiplier) + '}}'
        self.send(msg)

    def rotateDroneLeft(self, multiplier):
        msg = '{"primitiveControls": {"yawRightAmount": ' + str(-multiplier) + '}}'
        self.send(msg)

    def moveDrone(self, multiplierUp, multiplierForward, multiplierRight, multiplierYaw):
        msg = '{"primitiveControls": {"upAmount": ' + str(multiplierUp) + ', "pitchForwardAmount": ' + str(multiplierForward) + ', "rollRightAmount": ' + str(
            multiplierRight) + ', "yawRightAmount": ' + str(multiplierYaw) + '}}'
        self.send(msg)

    def getDroneState(self):
        msg = '{"getDroneState": "true"}'
        self.send(msg)

    def sendDroneGrade(self, grade):
        msg = '{"droneGrade": ' + str(grade) + '}'
        self.send(msg)


################################################################################

    def countdown_timer(self,seconds):
        while seconds > 0:
            print(f"Time left: {seconds} seconds")
            time.sleep(1)
            seconds=seconds - 1
        exit()  # if time finished, exit the program

#Function deacrese 1 point each second
    def decreaseEachSec(self,points):
        initializedScore=y["initializedScore"]
        while True:
            initializedScore=initializedScore-1
            time.sleep(1)
            print(f"points at the end: {initializedScore} points")


    def pointsDecreaseCollision(self,numOfCollision):
        costPerCollision=y["collisionCost"]
        pointsToDecrease=numOfCollision*costPerCollision
        return pointsToDecrease



