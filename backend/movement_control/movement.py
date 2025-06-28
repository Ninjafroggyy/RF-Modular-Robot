"""
movement.py — Simplified Movement Command Wrapper

Provides a lightweight helper function for sending movement commands to the robot.
While the frontend typically sends commands directly via the network module, this
wrapper allows for reuse in unit tests or scripts with a cleaner API.
"""

from backend.network_communication import network

# Set of allowed directions
ALLOWED = {"forward", "backward", "left", "right", "stop"}


def move(direction: str) -> None:
    """
    Send a movement command to the robot, if the direction is valid.

    Args:
        direction (str): One of 'forward', 'backward', 'left', 'right', or 'stop'.
    """
    if direction not in ALLOWED:
        print(f"[WARN] Invalid move: {direction}")
        return
    network.send({"type": "movement", "direction": direction})
