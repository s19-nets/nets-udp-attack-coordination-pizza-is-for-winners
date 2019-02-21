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

    def get_previous_sent_message(self):
        """Returns previous sent message in the packet manager."""
        try:
            return self.get_available_messages()[self.sent_msg - 1]
        except IndexError:
            print("{} has sent all messages".format(self.agent))
            return False

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
        # Check if retry command was sent # Make this smart (send lastAcked)
        if int(message[0]) == -1:
            print("Retry command received, reset packets to", message[1])
            self.set_send_msg(int(message[1]))
            return True
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

    def __init__(self, agent, server_address=50002, client_address=50001):
        """Create a protocol according to an agent."""
        self.pm = Packet_Manager(agent)  # This ensures correct agent
        self.agent = self.pm.agent
        self.server_address = ('localhost', server_address)
        self.client_address = ('localhost', client_address)
        self.send_sock = self._create_send_socket()
        self.recv_sock = self._create_recv_socket()

    def _create_send_socket(self):
        """Creates recv socket."""
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _create_recv_socket(self):
        """Creates a send socket with binding."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.agent == "client":
            sock.bind(self.client_address)
        else:
            sock.bind(self.server_address)
        if not sock:
            print("Couldn't bind sock")
            return None   # Handle this
        return sock

    def send_non_stop(self, wait=0):
        """Sends packets expecting receival."""
        pass

    def stop_and_wait(self, wait=3):
        """Implements a stop and wait protocol."""

        retries = 3

        # Client will send first msg then wait for ack, and continue
        while True:
            time.sleep(wait)  # Or else the True goes too fast
            read, send, errs = select.select(
                [self.recv_sock], [self.send_sock], [], wait)

            print("last ack{}, sent{}".format(
                self.pm.received_msg, self.pm.sent_msg))

            for s in read:
                if self.finished():
                    print("Messages have been finished, will not receive")
                    return False

                print("ready to read")  # Debugging
                data, addr = s.recvfrom(2048)
                if data:
                    print(data)  # Debugging
                    if self.recv(data):  # Validate data
                        continue
                    else:
                        time.sleep(2)
                        if retries > 0:
                            retries = retries - 1
                            continue
                        retries = 5
                        self.request_retry_send()
                else:
                    # No data received
                    print("No data yet")


            for s in send:
                print("ready to send")
                self.send()
                if self.finished():
                    print("Messages have been finished, will not send")
                    return False

            for s in errs:
                print("ups there are some errors")

    def request_retry_send(self):
        """Will send all packets from the beggining again upon request."""
        retry_msg = "-1, {}".format(self.pm.received_msg)
        print("Sent retry message", retry_msg)
        if self.agent == "client":
            self.send_sock.sendto(retry_msg.encode(), self.server_address)
            return True
        if self.agent == "server":
            self.send_sock.sendto(retry_msg.encode(), self.client_address)
            return True
        return False

    def send(self):
        """Send next message if ack was received."""
        # Check that client and server are on sync
        message = None
        if not self.proceed_send():
            # Resend message
            if self.pm.received_msg != 0:
                message = self.pm.get_previous_sent_message()
        else:
            # Send next message
            message = self.pm.send_next_message()
        if not message:
            print("Messages not started or ended!")
            return False
        # Client
        print("->Sending", message)
        if self.agent == "client":
            self.send_sock.sendto(message.encode(), self.server_address)
        # Server
        else:
            self.send_sock.sendto(message.encode(), self.client_address)

    def proceed_send(self):
        """Will ensure that the client and the server are on sync."""
        if self.agent == "client":
            # First message case
            if self.pm.received_msg == self.pm.sent_msg:
                print("Sending first message")
                return True
            print("Waiting for confirmation")
            return False

        if self.agent == "server":
            # First message case
            if self.pm.received_msg == self.pm.sent_msg:
                print("Waiting for initial msg")
                return False
            return True

        return False  # Something went terribly wrong

    def recv(self, message):
        """Validate received message."""
        if self.pm.validate_received_message(message.decode()):
            return True
        return False

    def finished(self):
        """Check if the protocol has finished."""
        num_messages = len(self.pm.get_available_messages())
        if (num_messages == self.pm.sent_msg
                and num_messages == self.pm.received_msg):
            return True
        return False


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
