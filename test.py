import socket
import time

if __name__ == '__main__':
    ip_portRecv = ("127.0.0.1", 3001)
    udp_socketRecv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # receiver socket (UDP) opened
    udp_socketRecv.bind(ip_portRecv)

    udp_socketSend = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # sender socket (UDP) opened
    ip_portSend = ("127.0.0.1", 3002)

    print("Waiting for message...")
    lst = []
    msg = '{"primitiveControls": {"upAmount": 1, "pitchForwardAmount": 1, "rollRightAmount": 0.5, "yawRightAmount": -0.5}, "getDroneState": "true"}'
    while True:
        currTime = time.time()

        udp_socketSend.sendto(msg.encode('utf-8'), ip_portSend)  # Send message to UE

        message = udp_socketRecv.recv(4096)  # Receive message from UE
        message_str = message.decode('utf-8')  # Convert message to string

        lst.append(time.time() - currTime)
        # print("Time taken: " + str(time.time() - currTime))
        print(message_str)
        print("Average time taken: " + str(sum(lst) / len(lst)))
        # time.sleep(0.1)
