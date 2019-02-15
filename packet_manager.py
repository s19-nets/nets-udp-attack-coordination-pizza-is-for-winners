"""Message protocol implementation."""
import socket
import time
import select

class Packet_Manager:
    """Packet class."""

    def __init__(self, agent):
        """Initializes a packet according to an agent (client or server)."""
        self.agent = self._validate_agent(agent)  # Saves agent
        self.received_msg = 0  # last_ACKed
        self.sent_msg = 0  # packet number

    def _get_agent(self):
        """Returns an agent for a packet (testing purposes)."""
        return self.agent

    @staticmethod
    def _validate_agent(agent):
        agent = agent.lower()
        if agent not in ['server', 'client']:
            print("Unkown agent. Please use either server or client")
            raise ValueError
        return agent

    def get_available_messages(self):
        """Gets available messages for either server or client."""
        # Messages available for the server
        server_msg = [
            "0, pong", "1, the enemy is ready for battle",
            "2, what is the best time for attack?", "3, 11?",
            "4, 11 it is. Confirm"]
        # Messages available for the client
        client_msg = [
            "0, ping", "1, let's coordinate an attack!",
            "2, what about 11", "3, Yes 11",
            "4, Confirmed 11"]
        if self.agent == "server":
            return server_msg
        return client_msg

    def send_requested_message(self, message_num):
        """Sends the message requested."""
        if message_num > len(self.get_available_messages()) or message_num < 0:
            print("Requested message #{} is out of range".format(message_num))
            return False
        return self.get_available_messages()[message_num]

    def send_next_message(self):
        """Will send next expected message."""
        try:
            msg = self.get_available_messages()[self.sent_msg]
            self.sent_msg = self.sent_msg + 1
            return msg
        except IndexError:
            print("No more messages available")
            return False

    def set_send_msg(self, message_num):
        """Sets the send message counter to message_num."""
        if message_num > len(self.get_available_messages()) or message_num < 0:
            print("Requested message #{} is out of range".format(message_num))
            return False
        self.sent_msg = message_num
        return True

    def get_current_sent_message(self):
        """Returns current sent message in the packet manager."""
        try:
            return self.get_available_messages()[self.sent_msg]
        except IndexError:
            print("{} has sent all messages".format(self.agent))
            return False

    def get_current_received_message(self):
        """Returns current received message in the packet manager."""
        print(self.received_msg)
        if self.received_msg <= 0:
            print("{} has not received any messages".format(self.agent))
            return False
        return self.get_available_messages()[self.received_msg - 1]

    def validate_received_message(self, message):
        """Validates that the received message is valid."""
        message = self._prepare_msg(message)
        if int(message[0]) != self.received_msg:  # Looking for next messag
            print("This is not the expected message")
            print("Expected msg #{}, obtained msg #{}".format(
                message[0], self.received_msg))
            return False
        print("Received correct message:", message)
        self.received_msg = self.received_msg + 1  # Update current message
        return True

    @staticmethod
    def _prepare_msg(message):
        try:
            message = message.split(",")
            # Returns tuple with message# and message text
            return (message[0], message[1])
        # Catch exception, and raise it again
        except IndexError:
            print("Unknown message")
            raise ValueError


class Attack_Protocol:
    """Attack protocol which will handle packet management."""

    def __init__(self, agent, address=5002):
        """Create a protocol according to an agent."""
        self.pm = Packet_Manager(agent)  # This ensures correct agent
        self.agent = self.pm.agent
        self.server_address = ('localhost', address)
        self.sock = self._create_socket()
        print("Created sock", self.sock)

    def _create_socket(self):
        """Creates a socket according to the agent. TODO add prints."""
        if self.agent == "client":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return self.sock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        return self.sock

    def stop_and_wait(self, wait=5):
        """Implements a stop and wait protocol."""
        # self.sock.setblocking(0)

        if self.agent == "client":
            # Send one message then wait for a response and continue.
            # Will stop untill all messages are sent
            # for _x in self.pm.get_available_messages():
            #     message = self.pm.send_next_message()
            message = "hi"
            inout = [self.sock]
            while 1:
                time.sleep(1)
                infds, outfds, errfds = select.select(inout, inout, [], 5)
                if infds:
                    buf = self.sock.recvfrom(1024)
                    if buf:
                        print('receive data:', buf)
                if outfds:
                    print("Sending Message:", message)
                    self.sock.sendto(str.encode(message), self.server_address)

        if self.agent == "server":
            inputs = [self.sock]
            while 1:
                time.sleep(1)
                infds, outfds, errfds = select.select(inputs, inputs, [], 5)
                if infds:
                    print(infds)
                    for fds in infds:
                        if fds is not self.sock:
                            # clientsock, clientaddr = fds.accept()
                            # inputs.append(clientsock)
                            print('connect from:', "somewhere")
                        else:
                            # print 'enter data recv'
                            data = fds.recvfrom(1024)
                            print(data)
                            if not data:
                                inputs.remove(fds)
                            else:
                                print(data)
                if outfds:
                    for fds in outfds:
                        msg = "Test"
                        print("Sending message", msg)
                        fds.sendto(str.encode(msg), self.server_address)






def _main():
    # Create a packet (manager) for a client
    # Create a packet (manager) for a server
    client_packet = Packet_Manager("client")
    server_packet = Packet_Manager("server")

    # Testing purposes
    print("client agent ->", client_packet._get_agent())
    print("server agent ->", server_packet._get_agent())

    # Get available messages for each packet manager
    client_msgs = client_packet.get_available_messages()
    server_msgs = server_packet.get_available_messages()
    print("client msgs ->", client_msgs)
    print("server msgs ->", server_msgs)

    # Start sending mensages and validating them

    # Test current received message
    print(server_packet.get_current_received_message())  # Should error

    # Send a message from the client to the server
    print("Validating client msg to server msg")
    server_packet.validate_received_message(
        client_packet.send_next_message())
    print(server_packet.get_current_received_message())
    # Send a message from the server to the client
    print("Validating server msg to server msg")
    client_packet.validate_received_message(
        server_packet.send_next_message())
    print(client_packet.get_current_received_message())


# Run main function
# _main()
