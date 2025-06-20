import unittest
from backend.movement_control import movement


""" EXAMPLE UNIT TESTS """

class TestMovement(unittest.TestCase):

    def test_valid_direction(self):
        """Test sending a valid movement command."""
        with self.assertLogs(level='INFO') as log:
            movement.send_movement_command("forward")
            # This should call network.send_data without error

    def test_invalid_direction(self):
        """Test sending an invalid direction."""
        with self.assertLogs(level='WARNING') as log:
            movement.send_movement_command("fly")
            self.assertIn("Invalid direction", log.output[0])


if __name__ == '__main__':
    unittest.main()
