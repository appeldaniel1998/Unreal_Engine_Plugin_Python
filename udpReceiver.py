import socket
import struct

UDP_IP = "127.0.0.1"  # replace with the IP address of the machine running Unreal Engine
UDP_PORT = 20001  # replace with the port number used in Unreal Engine

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
struct_format = '20f 3B'

print("Waiting for data...")
while True:
    data, addr = sock.recvfrom(1024)  # Receive data from the socket

    # Unpack the received data using the struct format
    unpacked_data = struct.unpack(struct_format, data)

    # Access the individual floats and integers in the unpacked data
    print(unpacked_data)
