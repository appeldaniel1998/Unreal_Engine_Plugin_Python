import json
import socket


class PublicDroneControl:
    def __init__(self, ip, port):
        """
        This function is used to initialize the PublicDroneControl object
        :param ip: IP address of the UE engine
        :param port: port number of the UE engine receiver socket (+1 is used for the sender socket)
        """
        ip_portRecv = (ip, port)
        self.udp_socketRecv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # receiver socket (UDP) opened
        self.udp_socketRecv.bind(ip_portRecv)

        self.udp_socketSend = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # sender socket (UDP) opened
        self.ip_portSend = (ip, port + 1)

    def send(self, msg):
        """
        This function is used to send a message to the UE engine
        :param msg: message to send to UE engine
        :return: None
        """
        self.udp_socketSend.sendto(msg.encode('utf-8'), self.ip_portSend)  # Send message to UE

    #  Primitive Controls -------------------------------------------------------

    def moveDroneUp(self, speedMultiplier):
        """
        This function is used to move the drone up
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneDown(self, speedMultiplier):
        """
        This function is used to move the drone down
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneForward(self, speedMultiplier):
        """
        This function is used to move the drone forward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneBackward(self, speedMultiplier):
        """
        This function is used to move the drone backward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneRight(self, speedMultiplier):
        """
        This function is used to move the drone right
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneLeft(self, speedMultiplier):
        """
        This function is used to move the drone left
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def rotateDroneRight(self, speedMultiplier):
        """
        This function is used to rotate the drone right
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def rotateDroneLeft(self, speedMultiplier):
        """
        This function is used to rotate the drone left
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def rotateCameraDown(self, speedMultiplier):
        """
        This function is used to rotate the camera down
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def rotateCameraUp(self, speedMultiplier):
        """
        This function is used to rotate the camera up
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    #  End Primitive Controls ---------------------------------------------------

    #  Advanced Controls --------------------------------------------------------

    def hoverDrone(self):
        """
        This function is used to hover the drone
        :return: None
        """
        msg = '{"controls": {"hover": "true"}}'
        self.send(msg)

    def rotateDroneXDegreesAtSpeed(self, degrees, speed=90):
        """
        This function is used to rotate the drone a certain number of degrees at a certain speed
        :param degrees: number of degrees to rotate
        :param speed: speed at which to rotate (in degrees per second)
        :return: None
        """
        msg = '{"controls": {"rotateXDegrees": ' + str(degrees) + ', "rotationSpeed": ' + str(speed) + '}}'
        self.send(msg)

    def rotateDroneTowardsLocation(self, x, y, z, speed=90):
        """
        This function is used to rotate the drone towards a certain location at a certain speed
        :param x: x coordinate of target location on UE grid
        :param y: y coordinate of target location on UE grid
        :param z: z coordinate of target location on UE grid
        :param speed: speed at which to rotate (in degrees per second)
        :return: None
        """
        msg = '{"controls": {"turnTowards": {"turnTowardsXVal": ' + str(x) + ', "turnTowardsYVal": ' + str(y) + ', "turnTowardsZVal": ' + str(
            z) + ', "turnTowardsSpeed": ' + str(speed) + '}}}'
        self.send(msg)

    def moveDroneToLocation(self, x, y, z, speed=2, turnWithMove=True):
        """
        This function is used to move the drone to a certain location at a certain speed
        :param x: x coordinate of target location on UE grid
        :param y: y coordinate of target location on UE grid
        :param z: z coordinate of target location on UE grid
        :param speed: speed at which to move (in meters per second)
        :param turnWithMove: boolean value, if true, drone will turn while moving to face the target location
        :return: None
        """
        if turnWithMove:  # turnWithMove is a boolean value, convert it to lowercase string
            turnWithMove = "true"
        else:
            turnWithMove = "false"

        msg = '{"controls": {"goto": {"gotoXVal": ' + str(x) + ', "gotoYVal": ' + str(y) + ', "gotoZVal": ' + str(z) + ', "gotoSpeed": ' + str(
            speed) + ', "turnWithMove": ' + turnWithMove + '}}}'
        self.send(msg)

    #  End Advanced Controls ----------------------------------------------------

    def getDroneState(self) -> json:
        """
        This function is used to get the current state of the drone
        The state includes the location of the drone (in UE grid coordinates) and the number of collisions up to that point
        :return: None
        """
        msg = '{"getDroneState": "true"}'
        self.send(msg)
        returnMsg = self.udp_socketRecv.recv(1024)  # Receive message from UE
        return json.loads(returnMsg.decode("utf-8"))

    def sendDroneGrade(self, grade):
        """
        This function is used to send the grade of the drone to the UE
        :param grade: grade of the drone (double)
        :return: None
        """
        msg = '{"droneGrade": ' + str(grade) + '}'
        self.send(msg)
