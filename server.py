"""Create a server to support pidgeon_attack protocol."""
import socket
import sys
import os
import packet_manager

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 5002)
print("starting up on {} port {}".format(server_address[0], server_address[1]))
sock.bind(server_address)

pm = packet_manager.Packet_Manager("server")

while True:
    # Wait to receive instruction to send file
    print('waiting to receive message')
    data, address = sock.recvfrom(512)

    # print("received {} bytes from {}".format(len(data), address))
    # print(data.decode())

    if data:
        # sent = sock.sendto(data, address)
        # print('sent {} bytes back to {}'.format(sent, address))
        print(data.decode())
        msg = pm.send_next_message()
        print("Sending message", msg)
