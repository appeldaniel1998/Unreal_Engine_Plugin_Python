import socket

if __name__ == '__main__':
    ip_portRecv = ("127.0.0.1", 20001)
    udp_socketRecv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # receiver socket (UDP) opened
    udp_socketRecv.bind(ip_portRecv)

    udp_socketSend = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # sender socket (UDP) opened
    ip_portSend = ("127.0.0.1", 20002)
    i = 0

    print("Waiting for message...")
    msg = "Hello"
    while True:
        message = udp_socketRecv.recv(4096)  # Receive message from UE
        message_str = message.decode('utf-8')  # Convert message to string
        msg = str(i) + ": " + message_str
        print(msg)
        i += 1

        udp_socketSend.sendto(msg.encode('utf-8'), ip_portSend)  # Send message to UE

