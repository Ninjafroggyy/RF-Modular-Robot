"""
    Handles robot movement commands and sends them to the robot via network.
"""

from backend.network_communication import network


ALLOWED_DIRECTIONS = ["forward", "backward", "left", "right", "stop"]


def send_movement_command(direction: str):
    """
        Send a movement command to the robot.

    Args:
        direction (str): One of 'forward', 'backward', 'left', 'right', 'stop'
    """
    if direction not in ALLOWED_DIRECTIONS:
        print(f"[WARN] Invalid direction: {direction}")
        return

    command = {"type": "movement", "direction": direction}
    network.send_data(command)
