"""
TCP command channel to the Raspberry Pi.
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


# ── Connection helpers ──────────────────────────────────────────────
def _open_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, CTRL_PORT))
    return sock


def connect() -> None:
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
    global _connected
    print(f"[↻] Reconnecting in {_RECONNECT_DELAY}s …")
    time.sleep(_RECONNECT_DELAY)
    connect()


# ── Public API ──────────────────────────────────────────────────────
def send(data: dict) -> None:
    """JSON-encode a command and send it to the Pi."""
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
    global _sock, _connected
    if _sock:
        _sock.close()
    _connected = False
