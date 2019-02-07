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
    pass
