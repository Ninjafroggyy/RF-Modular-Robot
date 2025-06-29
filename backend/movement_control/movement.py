""" Provides a helper function for sending movement commands to the robot. """
# Program file imports
from backend.network_communication import network

# Set of allowed directions
ALLOWED = {"forward", "backward", "left", "right", "stop"}


def move(direction: str):
    """ Send a movement command to the robot, if the direction is valid. """
    if direction not in ALLOWED:
        print(f"[WARN] Invalid move: {direction}")
        return
    network.send({"type": "movement", "direction": direction})
