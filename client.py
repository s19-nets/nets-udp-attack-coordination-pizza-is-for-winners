"""Client to support pidgeon_attack protocol."""

import socket
import packet_manager
# Create a socket and specify address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 5002)
print("Client starting up on {} port {}".format(server_address[0],
                                                server_address[1]))

# Create a protocol
client = packet_manager.Attack_Protocol("Client")
client.stop_and_wait()

# # Create a packet manager
# client = packet_manager.Packet_Manager("Client")
#
# for _x in client.get_available_messages():
#     message = client.send_next_message()
#     sock.sendto(str.encode(message), server_address)
