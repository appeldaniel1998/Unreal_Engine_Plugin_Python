import json
import socket
import threading
from queue import Queue

from Core.Coordinate import Coordinate
from Core.DroneState import DroneState
from Core.Target import Target


def extractMessageFromPrefix(prefix, message):
    # Split the message at the prefix and get the remainder
    parts = message.split(prefix, 1)  # The second argument '1' ensures splitting is done only once
    if len(parts) > 1:
        return parts[1]  # Return the part after the prefix
    return None  # Return None if the prefix is not found


def parseHitResult(hitResultMsg: str) -> Target or None:
    if hitResultMsg == 'None':
        return None

    parts = hitResultMsg.split()  # Splitting the message by spaces to get each part

    # Extract DisplayName and ClassName directly
    display_name = parts[0].split('=')[1]
    class_name = parts[1].split('=')[1]

    # Parse the X, Y, Z values from the rest of the string
    x = float(parts[2].split('=')[2])
    y = float(parts[3].split('=')[1])
    z = float(parts[4].split('=')[1])

    return Target(display_name, class_name, Coordinate(x, y, z))


def _validate_target_format(input_string: str) -> bool:
    try:
        # Attempt to parse the JSON string
        jsonData = json.loads(input_string)

        # Check for the presence and type of each required key
        if isinstance(jsonData.get("collisionCount"), int) and \
                isinstance(jsonData.get("positionXVal"), float) and \
                isinstance(jsonData.get("positionYVal"), float) and \
                isinstance(jsonData.get("positionZVal"), float):
            return True
        else:
            return False
    except json.JSONDecodeError:
        # If JSON decoding fails, the string is not in valid JSON format
        return False


class PublicDroneControl:
    def __init__(self, ip, port):
        """
        This function is used to initialize the PublicDroneControl object
        :param ip: IP address of the UE engine
        :param port: port number of the UE engine receiver socket (+1 is used for the sender socket)
        """
        self.udp_socketRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socketRecv.bind((ip, port))
        self.udp_socketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip_portSend = (ip, port + 1)

        self.message_queues = {
            'getDroneState': Queue(),
            'getDistanceToCameraDirection': Queue(),
            'getCameraTarget': Queue(),
            'SpawnXActors': Queue(),
            'GetTargetOfPoint': Queue(),
            'turnTowards': Queue(),
            'goto': Queue(),
            'turnCameraXDeg': Queue()
        }

        self.listener_thread = threading.Thread(target=self._listen)
        self.listener_thread.daemon = True
        self.listener_thread.start()

        self.spawnedActors = []

    def _listen(self):
        while True:
            data, _ = self.udp_socketRecv.recvfrom(4096)
            message = data.decode('utf-8')
            if 'getDroneState:' in message:
                self.message_queues['getDroneState'].put(extractMessageFromPrefix('getDroneState:', message))
            elif 'getDistanceToCameraDirection:' in message:
                self.message_queues['getDistanceToCameraDirection'].put(extractMessageFromPrefix('getDistanceToCameraDirection:', message))
            elif 'getCameraTarget:' in message:
                self.message_queues['getCameraTarget'].put(extractMessageFromPrefix('getCameraTarget:', message))
            elif 'SpawnXActors:' in message:
                self.message_queues['SpawnXActors'].put(extractMessageFromPrefix('SpawnXActors:', message))
            elif 'GetTargetOfPoint:' in message:
                self.message_queues['GetTargetOfPoint'].put(extractMessageFromPrefix('GetTargetOfPoint:', message))
            elif 'turnTowards:' in message:
                self.message_queues['turnTowards'].put(extractMessageFromPrefix('turnTowards:', message))
            elif 'goto:' in message:
                self.message_queues['goto'].put(extractMessageFromPrefix('goto:', message))
            elif 'turnCameraXDeg:' in message:
                self.message_queues['turnCameraXDeg'].put(extractMessageFromPrefix('turnCameraXDeg:', message))

    def _send(self, msg: str) -> None:
        """
        This function is used to send a message to the UE engine
        :param msg: message to send to UE engine
        :return: None
        """
        self.udp_socketSend.sendto(msg.encode('utf-8'), self.ip_portSend)  # Send the message to the UE engine

    #  Primitive Controls -------------------------------------------------------

    def moveDroneUp(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone up
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(speedMultiplier) + '}}'
        self._send(msg)

    def moveDroneDown(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone down
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"upAmount": ' + str(-speedMultiplier) + '}}'
        self._send(msg)

    def moveDroneForward(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone forward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(speedMultiplier) + '}}'
        self._send(msg)

    def moveDroneBackward(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone backward
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"pitchForwardAmount": ' + str(-speedMultiplier) + '}}'
        self._send(msg)

    def moveDroneRight(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone right
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(speedMultiplier) + '}}'
        self._send(msg)

    def moveDroneLeft(self, speedMultiplier: float) -> None:
        """
        This function is used to move the drone left
        :param speedMultiplier: speed at which to move the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"rollRightAmount": ' + str(-speedMultiplier) + '}}'
        self._send(msg)

    def rotateDroneRight(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the drone right
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(speedMultiplier) + '}}'
        self._send(msg)

    def rotateDroneLeft(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the drone left
        :param speedMultiplier: speed at which to rotate the drone (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"yawRightAmount": ' + str(-speedMultiplier) + '}}'
        self._send(msg)

    def rotateCameraDown(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the camera down
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(speedMultiplier) + '}}'
        self._send(msg)

    def rotateCameraUp(self, speedMultiplier: float) -> None:
        """
        This function is used to rotate the camera up
        :param speedMultiplier: speed at which to rotate the camera (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"cameraDownAmount": ' + str(-speedMultiplier) + '}}'
        self._send(msg)

    #  End Primitive Controls ---------------------------------------------------

    #  Advanced Controls --------------------------------------------------------

    def hoverDrone(self) -> None:
        """
        This function is used to hover the drone
        :return: None
        """
        msg = '{"controls": {"hover": "true"}}'
        self._send(msg)

    def rotateDroneXDegreesAtSpeed(self, degrees: float, speed: float = 90) -> None:
        """
        This function is used to rotate the drone a certain number of degrees at a certain speed
        :param degrees: number of degrees to rotate
        :param speed: speed at which to rotate (in degrees per second)
        :return: None
        """
        msg = '{"controls": {"rotateXDegrees": ' + str(degrees) + ', "rotationSpeed": ' + str(speed) + '}}'
        self._send(msg)

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
        self._send(msg)
        message = self.message_queues['turnTowards'].get()  # This will block until an item is available
        if message == 'Done':
            return
        else:
            raise Exception(f"Error in turning towards location: {message}")

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

        msg = ('{"controls": {"goto": {"gotoXVal": ' + str(x) + ', "gotoYVal": ' + str(y) + ', "gotoZVal": ' + str(z) + ', "gotoSpeed": ' +
               str(speed) + ', "turnWithMove": ' + turnWithMove + '}}}')
        self._send(msg)

        message = self.message_queues['goto'].get()  # This will block until an item is available
        if message == 'Done':
            return
        else:
            raise Exception(f"Error in moving to location: {message}")

    def turnCameraXDegreesAtSpeed(self, degrees: float, speedMultiplier: float = 60) -> None:
        """
        This function is used to turn the camera a certain number of degrees at a certain speed
        :param degrees: number of degrees to turn
        :param speedMultiplier: speed at which to turn (multiplier of default speed)
        :return: None
        """
        msg = '{"controls": {"turnCameraXDeg": {"degrees": ' + str(degrees) + ', "speedMultiplier": ' + str(speedMultiplier) + '}}}'
        self._send(msg)

        message = self.message_queues['turnCameraXDeg'].get()  # This will block until an item is available
        if message == 'Done':
            return
        else:
            raise Exception(f"Error in turning camera: {message}")

    #  End Advanced Controls ----------------------------------------------------

    #  Drone Vision -------------------------------------------------------------

    def getDroneState(self) -> DroneState:
        """
        This function is used to get the current state of the drone
        The state includes the location of the drone (in UE grid coordinates) and the number of collisions up to that point
        :return: None
        """
        msg = '{"getDroneState": "true"}'
        self._send(msg)
        message = self.message_queues['getDroneState'].get()  # This will block until an item is available
        json_message = json.loads(message)
        return DroneState(
            Coordinate(json_message["positionXVal"], json_message["positionYVal"], json_message["positionZVal"]),
            json_message["collisionCount"]
        )

    def sendDroneGrade(self, grade: float) -> None:
        """
        This function is used to send the grade of the drone to the UE
        :param grade: grade of the drone (double)
        :return: None
        """
        msg = '{"droneGrade": ' + str(grade) + '}'
        self._send(msg)

    def getDistanceToCameraDirection(self) -> float:
        """
        This function is used to get the distance to the nearest object in the direction of where the camera is facing
        :return: distance to nearest object in direction of camera in meters
        """
        msg = '{"getDistanceToCameraDirection": "true"}'
        self._send(msg)

        # Receiving distance from UE in UE units, e.g. centimeters. Have to convert to meters
        message = self.message_queues['getDistanceToCameraDirection'].get()  # This will block until an item is available
        return float(message) / 100  # Convert to meters

    def getCameraTarget(self) -> Target or None:
        """
        This function is used to get the information regarding the nearest object in the direction of where the camera is facing
        :return:    Target object containing:
                        Display name of target,
                        Class name of target,
                        Location of target (in X, Y, Z coordinates in UE units)
        """
        msg = '{"getCameraTarget": "true"}'
        self._send(msg)
        message = self.message_queues['getCameraTarget'].get()  # This will block until an item is available
        # Received string in the form: 'DisplayName=Cube ClassName=StaticMeshActor Location=X=19410.000 Y=33114.466 Z=98.913' or 'None' if no target is detected
        return parseHitResult(message)

    def getTargetOfPoint(self, coordinateX: float, coordinateY: float) -> Target or None:
        """
        This function is used to get the information regarding the nearest object in the direction of a set of coordinates on screen (in 2D space).
        UE parses this into 3D space and returns the relevant information.
        The coordinates passed should be of the simulation only, without borders or any blank spaces
        :param coordinateX: Normalized X coordinate in 2D space of the simulation (on screen)
        :param coordinateY: Normalized Y coordinate in 2D space of the simulation (on screen)
        :return:    Target object containing:
                        Display name of target,
                        Class name of target,
                        Location of target (in X, Y, Z coordinates in UE units)
        """
        msg = ('{"GetTargetOfPoint": {"xVal": ' + str(coordinateX) + ', "yVal": ' + str(coordinateY) + '}}')
        self._send(msg)
        targetOfPointString = self.message_queues['GetTargetOfPoint'].get()  # Blocks until an item is available
        # Received string in the form: 'DisplayName=Cube ClassName=StaticMeshActor Location=X=19410.000 Y=33114.466 Z=98.913' or 'None' if no target is detected
        return parseHitResult(targetOfPointString)

    #  End Drone Vision ---------------------------------------------------------

    #  Map Controls -------------------------------------------------------------

    def requestDaytimeChange(self, addDegrees: float) -> None:
        """
        This function is used to request a change in the time of day in the simulation.
        :param addDegrees: add this number of degrees to the current positioning of the sun (direction of the light)
        """
        msg = '{"DaytimeChangeRequested": ' + str(addDegrees) + '}'
        self._send(msg)

    def spawnXActors(self, numOfActorsToSpawn: int) -> list[tuple[int, int, int]] or None:
        """
        The method should be called at start of simulation
        This method spawns people NPC in the simulation, where numOfActorsToSpawn is the number of actors which will be spawned randomly.
        All NPC are randomized in their appearance (male/female/skin and body types/clothing)
        :param numOfActorsToSpawn: The number of actors which will be spawned randomly (max value is 150)
        :return: Returns the list locations (x, y, z coordinates) of the spawned actors.
        """

        if numOfActorsToSpawn > 150:
            numOfActorsToSpawn = 150
        msg = '{"SpawnXActors": ' + str(numOfActorsToSpawn) + '}'
        self._send(msg)
        print("Sent message to spawn actors")
        actorLocationsString = self.message_queues['SpawnXActors'].get()  # Blocks until response is received
        actorLocationsStringJson = json.loads(actorLocationsString)

        # Parse the JSON data into a list of tuples
        coordinates = []
        for i in range(len(actorLocationsStringJson) // 3):
            x = actorLocationsStringJson[f"{i}-XLoc"]
            y = actorLocationsStringJson[f"{i}-YLoc"]
            z = actorLocationsStringJson[f"{i}-ZLoc"]
            coordinates.append(Coordinate(x, y, z))

        self.spawnedActors = coordinates
        return coordinates

    #  End Map Controls ---------------------------------------------------------

    #  Simulation Methods -------------------------------------------------------

    def verifyAndDestroyActorFromCamera(self) -> bool:
        """
        Method to verify that the target is a spawned actor, and if verified, remove the actor from the simulation

        :return: True if verified, false otherwise
        """
        target = self.getCameraTarget()

        if target is None:
            return False

        if target.position in self.spawnedActors:
            index = self.spawnedActors.index(target.position)  # Get the index of the actor in the list
            msg = '{"DestroyActor": ' + str(index) + '}'
            self._send(msg)
            return True
        return False

    def verifyAndDestroyActorFromPoint(self, normalizedX, normalizedY) -> bool:
        """
        Method to verify that the target is a spawned actor, and if verified, remove the actor from the simulation

        :return: True if verified, false otherwise
        """
        target = self.getTargetOfPoint(normalizedX, normalizedY)

        if target is None:
            return False

        if target.position in self.spawnedActors:
            index = self.spawnedActors.index(target.position)  # Get the index of the actor in the list
            msg = '{"DestroyActor": ' + str(index) + '}'
            self._send(msg)
            return True
        return False

    #  End Simulation Methods ---------------------------------------------------
