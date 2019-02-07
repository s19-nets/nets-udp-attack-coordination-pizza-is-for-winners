"""Message protocol implementation."""


class Packet_Manager:
    """Packet class."""

    def __init__(self, agent):
        """Initializes a packet according to an agent (client or server)."""
        self.agent = self._validate_agent(agent)  # Saves agent
        self.received_msg = 0
        self.sent_msg = 0

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
        server_msg = ["0, pong", "1, test"]
        # Messages available for the client
        client_msg = ["0, ping", "1, test"]
        if self.agent == "server":
            return server_msg
        return client_msg

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

    def send_requested_message(self, message_num):
        """Sends the message requested."""
        if message_num > len(self.get_available_messages()):
            print("Requested message #{} is out of range".format(message_num))
            raise ValueError
        return self.get_available_messages()[message_num]

    def send_next_message(self):
        """Will send next expected message."""
        try:
            msg = self.get_available_messages()[self.sent_msg]
            self.sent_msg = self.sent_msg + 1
            return msg
        except ValueError:
            print("No more messages available")
            raise ValueError

    def set_send_msg(self, message_num):
        """Sets the send message counter to message_num."""
        if message_num > len(self.get_available_messages()):
            print("Requested message #{} is out of range".format(message_num))
            raise ValueError
        self.sent_msg = message_num
        return True

    @staticmethod
    def _prepare_msg(message):
        try:
            message = message.split(",")
            # Returns tuple with message# and message text
            return (message[0], message[1])
        # Catch exception, and raise it again
        except ValueError:
            print("Unknown message")
            raise ValueError

    def get_current_received_message(self):
        """Returns current received message in the packet manager."""
        print(self.received_msg)
        if self.received_msg <= 0:
            print("{} has not received any messages".format(self.agent))
            return False
        return self.get_available_messages()[self.received_msg - 1]

    def get_current_sent_message(self):
        """Returns current sent message in the packet manager."""
        try:
            return self.get_available_messages()[self.sent_msg]
        except ValueError:
            print("{} has sent all messages".format(self.agent))
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
_main()
