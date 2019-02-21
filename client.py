"""Client to support pidgeon_attack protocol."""

import socket
import packet_manager

# Create a protocol
proto = packet_manager.Attack_Protocol("client")
proto.stop_and_wait()

# # Create a packet manager
# client = packet_manager.Packet_Manager("Client")
#
# for _x in client.get_available_messages():
#     message = client.send_next_message()
#     sock.sendto(str.encode(message), server_address)
