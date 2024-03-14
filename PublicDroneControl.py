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

    def send(self, msg: str) -> None:
        """
        This function is used to send a message to the UE engine
        :param msg: message to send to UE engine
        :return: None
        """
        self.udp_socketSend.sendto(msg.encode('utf-8'), self.ip_portSend)  # Send message to UE

    #  Primitive Controls -------------------------------------------------------

    def moveDroneUp(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone up
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneDown(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone down
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneForward(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone forward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneBackward(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone backward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneRight(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone right
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def moveDroneLeft(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone left
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def rotateDroneRight(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the drone right
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def rotateDroneLeft(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the drone left
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    def rotateCameraDown(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the camera down
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(speedMultiplier) + '}}'
        self.send(msg)

    def rotateCameraUp(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the camera up
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(-speedMultiplier) + '}}'
        self.send(msg)

    #  End Primitive Controls ---------------------------------------------------

    #  Advanced Controls --------------------------------------------------------

    def hoverDrone(self) -> None:
        """
        This function is used to hover the drone
        :return: None
        """
        msg = '{"controls": {"hover": "true"}}'
        self.send(msg)

    def rotateDroneXDegreesAtSpeed(self, degrees: float, speed: float = 90) -> None:
        """
        This function is used to rotate the drone a certain number of degrees at a certain speed
        :param degrees: number of degrees to rotate
        :param speed: speed at which to rotate (in degrees per second)
        :return: None
        """
        msg = '{"controls": {"rotateXDegrees": ' + str(degrees) + ', "rotationSpeed": ' + str(speed) + '}}'
        self.send(msg)

    def rotateDroneTowardsLocation(self, x: float, y: float, z: float, speed: float = 90) -> None:
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

    def moveDroneToLocation(self, x: float, y: float, z: float, speed: float = 2, turnWithMove: bool = True) -> None:
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

    def sendDroneGrade(self, grade: float) -> None:
        """
        This function is used to send the grade of the drone to the UE
        :param grade: grade of the drone (double)
        :return: None
        """
        msg = '{"droneGrade": ' + str(grade) + '}'
        self.send(msg)

    def getDistanceToCameraDirection(self) -> float:
        """
        This function is used to get the distance to the nearest object in the direction of where the camera is facing
        :return: distance to nearest object in direction of camera in meters
        """
        msg = '{"getDistanceToCameraDirection": "true"}'
        self.send(msg)
        returnMsg = self.udp_socketRecv.recv(1024).decode("utf-8")  # Received distance from UE in UE units, e.g. centimeters. Have to convert to meters
        return float(returnMsg) / 100  # Converting to meters

    def getCameraTarget(self) -> tuple[str, str, tuple[float, float, float]]:
        """
        This function is used to get the location of the nearest object in the direction of where the camera is facing
        :return:    Display name of target,
                    Class name of target,
                    Location of target (in X, Y, Z coordinates in UE units)
        """
        msg = '{"getCameraTarget": "true"}'
        self.send(msg)
        returnMsg = self.udp_socketRecv.recv(1024).decode("utf-8")
        # Received string in the form: 'DisplayName=Cube ClassName=StaticMeshActor Location=X=19410.000 Y=33114.466 Z=98.913'

        parts = returnMsg.split()  # Splitting the message by spaces to get each part

        # Extract DisplayName and ClassName directly
        display_name = parts[0].split('=')[1]
        class_name = parts[1].split('=')[1]

        # Parse the X, Y, Z values from the rest of the string
        x = float(parts[2].split('=')[2])
        y = float(parts[3].split('=')[1])
        z = float(parts[4].split('=')[1])

        return display_name, class_name, (x, y, z)
