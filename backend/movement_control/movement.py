"""
Thin convenience wrapper for movement commands.
Frontend already calls network.send() directly, but this can be reused in tests.
"""
from backend.network_communication import network

ALLOWED = {"forward", "backward", "left", "right", "stop"}


def move(direction: str) -> None:
    if direction not in ALLOWED:
        print(f"[WARN] Invalid move: {direction}")
        return
    network.send({"type": "movement", "direction": direction})
