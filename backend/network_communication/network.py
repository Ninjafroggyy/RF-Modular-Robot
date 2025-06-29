"""
    Handles the network connection used to send JSON-formatted control commands from the laptop application to the
    Raspberry Pi robot over a  TCP socket.
"""
# Library imports
from __future__ import annotations
from typing import Optional
import json
import socket
import time
# Program file imports
from backend.config import HOST, CTRL_PORT

_RECONNECT_DELAY = 3  # seconds
_sock: Optional[socket.socket] = None
_connected = False


def _open_socket():
    """ Create and connect a new TCP socket to the Pi. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, CTRL_PORT))
    return sock


def connect():
    """ Attempt to establish a connection to the Raspberry Pi. """
    global _sock, _connected
    if _connected:
        return
    try:
        _sock = _open_socket()
        _connected = True
        print(f"MOVEMENT CONTROL: connected to {HOST}:{CTRL_PORT}")
    except Exception as exc:
        _connected = False
        print(f"MOVEMENT CONTROL connection failed: {exc}")


def _reconnect():
    """ Wait briefly and attempt to reconnect to the Pi. """
    global _connected
    print(f"Reconnecting in {_RECONNECT_DELAY}s …")
    time.sleep(_RECONNECT_DELAY)
    connect()


def send(data: dict):
    """ Send a JSON-encoded command to the Raspberry Pi. """
    global _sock, _connected
    if not _connected:
        connect()
        if not _connected:
            return

    try:
        _sock.sendall(json.dumps(data).encode() + b"\n")
    except Exception as exc:
        print(f"MOVEMENT CONTROL send failed: {exc}")
        _connected = False
        _reconnect()


def disconnect():
    """ Close the TCP connection to the Raspberry Pi. """
    global _sock, _connected
    if _sock:
        _sock.close()
    _connected = False
