"""
network.py — TCP Command Channel to Raspberry Pi

Handles the network connection used to send JSON-formatted control commands
from the laptop application to the Raspberry Pi robot over a persistent TCP socket.

Supports automatic reconnection and simple JSON message framing.
"""

from __future__ import annotations

import json
import socket
import time
from typing import Optional

from backend.config import HOST, CTRL_PORT

_RECONNECT_DELAY = 3  # seconds
_sock: Optional[socket.socket] = None
_connected = False


# ── Connection Helpers ─────────────────────────────────────────────
def _open_socket() -> socket.socket:
    """
    Create and connect a new TCP socket to the Pi.

    Returns:
        A connected socket object.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, CTRL_PORT))
    return sock


def connect() -> None:
    """
    Attempt to establish a connection to the Raspberry Pi.

    If already connected, this is a no-op.
    """
    global _sock, _connected
    if _connected:
        return
    try:
        _sock = _open_socket()
        _connected = True
        print(f"[✓] Ctrl: connected to {HOST}:{CTRL_PORT}")
    except Exception as exc:
        _connected = False
        print(f"[✗] Ctrl connection failed: {exc}")


def _reconnect() -> None:
    """
    Wait briefly and attempt to reconnect to the Pi.
    """
    global _connected
    print(f"[↻] Reconnecting in {_RECONNECT_DELAY}s …")
    time.sleep(_RECONNECT_DELAY)
    connect()


# ── Public API ─────────────────────────────────────────────────────
def send(data: dict) -> None:
    """
    Send a JSON-encoded command to the Raspberry Pi.

    Args:
        data (dict): The message to send. Will be encoded as a JSON string.
    """
    global _sock, _connected
    if not _connected:
        connect()
        if not _connected:
            return

    try:
        _sock.sendall(json.dumps(data).encode() + b"\n")
    except Exception as exc:
        print(f"[✗] Ctrl send failed: {exc}")
        _connected = False
        _reconnect()


def disconnect() -> None:
    """
    Close the TCP connection to the Raspberry Pi.
    """
    global _sock, _connected
    if _sock:
        _sock.close()
    _connected = False
