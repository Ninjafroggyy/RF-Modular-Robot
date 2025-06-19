"""
    Handles robot movement commands and sends them to the robot via network.
"""

from backend import network_communication


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
    network_communication.send_data(command)
