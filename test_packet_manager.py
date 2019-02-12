"""Test cases for packet_manager module."""
import pytest
import packet_manager as pm


def test_init():
    """Test __init__ as client and server."""
    # Test client
    client = pm.Packet_Manager("Client")
    assert client.agent == "client"
    # Test server
    server = pm.Packet_Manager("Server")
    assert server.agent == "server"
    # Test invalid
    with pytest.raises(ValueError):
        pm.Packet_Manager("Invalid")


def test_get_available_messages():
    """Test get_available_messages."""
    client = pm.Packet_Manager("Client")
    server = pm.Packet_Manager("Server")
    client_messages = client.get_available_messages()
    print(client_messages)
    assert client_messages is not None
    server_messages = server.get_available_messages()
    print(server_messages)
    assert server_messages is not None


def test_send_requested_message():
    """Test send_requested_message."""
    client = pm.Packet_Manager("Client")
    client_msgs_len = len(client.get_available_messages())

    # Test incorrect index for requested message (less than size)
    msg = client.send_requested_message(-1)  # Can't be negative size
    assert msg is False

    # Test incorrect index for requested message (more than size)
    msg = client.send_requested_message(client_msgs_len+1)
    assert msg is False

    # Test correct index (first message)
    assert client.send_requested_message(0) is not None


def test_send_next_message():
    """Test send_next_message."""
    client = pm.Packet_Manager("Client")

    # Test first message
    msg = client.send_next_message()
    print(msg)
    assert extract_msg_index(msg) == 0

    # Test second message
    msg = client.send_next_message()
    print(msg)
    assert extract_msg_index(msg) == 1

    # Test out of bounds index message
    client = pm.Packet_Manager("Client")  # Create a new client
    for _x in client.get_available_messages():
        client.send_next_message()


def test_set_send_msg():
    """Test set_send_msg."""
    client = pm.Packet_Manager("Client")
    client_msgs_len = len(client.get_available_messages())

    # Check that current messsage nuber is 0
    msg = client.get_current_sent_message()
    assert extract_msg_index(msg) == 0

    # Test incorrect index for send index message (less than size)
    msg = client.set_send_msg(-1)  # Can't be negative size
    assert msg is False

    # Test incorrect index for send index message (more than size)
    msg = client.set_send_msg(client_msgs_len+1)
    assert msg is False

    # Test correct index for send index message
    msg = client.set_send_msg(0)
    assert msg is True


def test_current_sent_message():
    """Test current sent message."""
    client = pm.Packet_Manager("Client")
    server = pm.Packet_Manager("Server")

    # Test no sent messages
    assert client.get_current_sent_message() is not False
    assert server.get_current_sent_message() is not False

    # Send multiple messages to reach the lenght of available messages
    client_msgs_len = len(client.get_available_messages())
    server_msgs_len = len(server.get_available_messages())
    # exhaust client msgs
    for _x in range(client_msgs_len):
        client.send_next_message()
    # exhaust server msgs
    for _x in range(server_msgs_len):
        server.send_next_message()

    # Test that no more msgs are available to be sent
    assert client.get_current_sent_message() is False
    assert server.get_current_sent_message() is False


def test_current_received_message():
    """Test current received message."""
    client = pm.Packet_Manager("Client")
    server = pm.Packet_Manager("Server")

    # Test no received messages
    assert client.get_current_received_message() is False
    assert server.get_current_received_message() is False

    # Send one message (server -> client) and test that it was received
    s_msg = server.send_next_message()
    client.validate_received_message(s_msg)
    msg = client.get_current_received_message()
    assert msg is not False  # A msg was received

    # Send one more message (server -> client) and test that it was received
    s_msg = server.send_next_message()
    client.validate_received_message(s_msg)
    msg = client.get_current_received_message()
    assert msg is not False  # A msg was received


def test_validate_received_message():
    """Test validate_received_message."""
    client = pm.Packet_Manager("Client")

    # Validate unknown message
    with pytest.raises(ValueError):
        client.validate_received_message("Unknown Message Format")

    # Validate incorrect index
    assert client.validate_received_message("-1, Incorrect order") is False

    # Validate correct index
    assert client.validate_received_message("0, Correct msg order") is True

    # Validate next correct index
    assert client.validate_received_message("1, Correct msg order 2") is True

    # Validate same message index
    assert client.validate_received_message("1, Correct msg order 2") is False


def extract_msg_index(message):
    """Extracts the index out of a message."""
    message = message.split(",")
    return int(message[0])
