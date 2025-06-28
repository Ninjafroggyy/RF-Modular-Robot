import unittest
from unittest.mock import patch, MagicMock
import json

from backend.network_communication import network


class TestNetworkModule(unittest.TestCase):

    def setUp(self):
        # Reset state before each test
        network._sock = None
        network._connected = False

    @patch("backend.network_communication.network._open_socket")
    def test_connect_success(self, mock_open_socket):
        mock_sock = MagicMock()
        mock_open_socket.return_value = mock_sock

        network.connect()

        self.assertTrue(network._connected)
        self.assertIs(network._sock, mock_sock)
        mock_open_socket.assert_called_once()

    @patch("backend.network_communication.network._open_socket", side_effect=Exception("connection failed"))
    def test_connect_failure(self, mock_open_socket):
        network.connect()

        self.assertFalse(network._connected)
        self.assertIsNone(network._sock)

    @patch("backend.network_communication.network._open_socket")
    def test_send_success(self, mock_open_socket):
        mock_sock = MagicMock()
        mock_open_socket.return_value = mock_sock

        # Send command after mock connection established
        test_data = {"type": "movement", "direction": "forward"}
        network.send(test_data)

        expected = json.dumps(test_data).encode() + b"\n"
        mock_sock.sendall.assert_called_once_with(expected)

    @patch("backend.network_communication.network._open_socket")
    def test_send_fails_and_reconnects(self, mock_open_socket):
        # First connection works
        mock_sock = MagicMock()
        mock_sock.sendall.side_effect = Exception("socket write failed")
        mock_open_socket.return_value = mock_sock

        with patch("backend.network_communication.network._reconnect") as mock_reconnect:
            test_data = {"type": "movement", "direction": "backward"}
            network.send(test_data)
            mock_reconnect.assert_called_once()
            self.assertFalse(network._connected)

    @patch("backend.network_communication.network._open_socket", side_effect=Exception("can't connect"))
    def test_send_aborts_if_unable_to_connect(self, mock_open_socket):
        # Will attempt to connect but fail
        test_data = {"type": "noop"}
        network.send(test_data)  # Should not raise, just silently skip
        self.assertFalse(network._connected)

    def test_disconnect(self):
        mock_sock = MagicMock()
        network._sock = mock_sock
        network._connected = True

        network.disconnect()

        mock_sock.close.assert_called_once()
        self.assertFalse(network._connected)


if __name__ == "__main__":
    unittest.main()
