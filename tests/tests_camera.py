import unittest
from unittest.mock import patch, MagicMock
from backend.camera_control import camera


class TestCameraStream(unittest.TestCase):

    @patch("backend.camera_control.camera._decode")
    @patch("backend.camera_control.camera.socket.socket")
    def test_camera_stream_loop_extracts_and_decodes_frame(self, mock_socket_class, mock_decode):
        # Prepare fake JPEG frame (with correct SOI and EOI markers)
        fake_jpg = b"\xff\xd8FAKEIMAGE\xff\xd9"
        frame_bytes = fake_jpg + fake_jpg + b""  # two full frames
        mock_sock = MagicMock()
        mock_sock.recv.side_effect = [frame_bytes, b""]  # simulate full read, then EOF
        mock_socket_class.return_value = mock_sock

        # Fake decode output
        mock_decode.return_value = (b"decoded_frame", (320, 240))

        # Clear any previously stored frame
        camera._latest = None

        # Call stream loop directly (not in a thread)
        camera.camera_stream_loop()

        # Verify that decode was called with correct frame(s)
        mock_decode.assert_called_with(fake_jpg)

        # Check if latest frame was updated correctly
        latest = camera.get_latest()
        self.assertIsNotNone(latest)
        self.assertEqual(latest[0], b"decoded_frame")
        self.assertEqual(latest[1], (320, 240))

        # Check socket was closed
        mock_sock.close.assert_called_once()

    def test_get_latest_returns_none_initially(self):
        # Should be None before any frames are received
        camera._latest = None
        self.assertIsNone(camera.get_latest())


if __name__ == "__main__":
    unittest.main()
