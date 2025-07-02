import unittest
from unittest.mock import patch, MagicMock
from backend.audio_output.audio import AudioReceiver


class TestAudioReceiver(unittest.TestCase):

    @patch("backend.audio_output.audio.pyaudio.PyAudio")
    @patch("backend.audio_output.audio.socket.socket")
    def test_start_and_stop(self, mock_socket_class, mock_pyaudio_class):
        # Setup mocks
        mock_sock = MagicMock()
        mock_stream = MagicMock()
        mock_socket_class.return_value = mock_sock
        mock_pyaudio_class.return_value.open.return_value = mock_stream

        receiver = AudioReceiver()
        receiver._CHUNK = 4  # Reduce chunk size for faster loop

        # Simulate audio stream and then EOF
        mock_sock.recv.side_effect = [b"\x00\x01", b"\x02\x03", b""]

        # Start and stop the receiver
        receiver.start()
        receiver._thread.join(timeout=1)
        receiver.stop()

        # Check key interactions occurred
        mock_socket_class.assert_called_once()
        mock_sock.connect.assert_called_once()
        mock_pyaudio_class.return_value.open.assert_called_once()
        mock_stream.write.assert_any_call(b"\x00\x01")
        mock_stream.write.assert_any_call(b"\x02\x03")

        # Allow multiple close calls but check at least once
        self.assertGreaterEqual(mock_stream.stop_stream.call_count, 1)
        self.assertGreaterEqual(mock_stream.close.call_count, 1)
        self.assertGreaterEqual(mock_sock.close.call_count, 1)

    def test_double_start_prevention(self):
        receiver = AudioReceiver()
        receiver._thread = MagicMock()
        receiver._thread.is_alive.return_value = True

        receiver.start()
        self.assertTrue(receiver._thread.is_alive())  # Should still be running, not restarted


if __name__ == "__main__":
    unittest.main()
