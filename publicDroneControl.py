import socket


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
