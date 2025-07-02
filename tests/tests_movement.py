import unittest
from unittest.mock import patch

# Import the move function from movement module
from backend.movement_control.movement import move


class TestMovement(unittest.TestCase):

    @patch("backend.movement_control.movement.network.send")
    def test_valid_directions(self, mock_send):
        # Test each valid direction
        for direction in ["forward", "backward", "left", "right", "stop"]:
            with self.subTest(direction=direction):
                move(direction)
                mock_send.assert_called_with({"type": "movement", "direction": direction})
                mock_send.reset_mock()  # Clear call history between subtests

    @patch("backend.movement_control.movement.network.send")
    def test_invalid_direction(self, mock_send):
        # Send an invalid command
        move("jump")
        # Should not call send
        mock_send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
