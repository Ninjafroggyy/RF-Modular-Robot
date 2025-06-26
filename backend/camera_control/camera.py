"""
Receive MJPEG frames over TCP and store latest raw RGB bytes.
Frontend converts to pygame Surface.
"""

import io
import socket
import threading
from typing import Optional, Tuple

from PIL import Image

from backend.config import HOST, CAMERA_PORT

_BUFFER      = 4096
_JPEG_SOI    = b"\xff\xd8"
_JPEG_EOI    = b"\xff\xd9"

_frame_lock  = threading.Lock()
_latest: Optional[Tuple[bytes, Tuple[int, int]]] = None  # (rgb_bytes, (w,h))


def _decode(jpg_bytes: bytes) -> Tuple[bytes, Tuple[int, int]]:
    img = Image.open(io.BytesIO(jpg_bytes)).convert("RGB")
    return img.tobytes(), img.size


def camera_stream_loop() -> None:
    global _latest
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, CAMERA_PORT))
        print(f"[✓] Cam: connected to {HOST}:{CAMERA_PORT}")
    except Exception as exc:
        print(f"[✗] Cam connection failed: {exc}")
        return

    buf = b""
    try:
        while True:
            chunk = sock.recv(_BUFFER)
            if not chunk:
                break
            buf += chunk

            while True:
                start = buf.find(_JPEG_SOI)
                if start == -1:
                    break
                end = buf.find(_JPEG_EOI, start)
                if end == -1:
                    break

                jpg = buf[start:end + 2]
                buf = buf[end + 2:]

                try:
                    rgb, size = _decode(jpg)
                    with _frame_lock:
                        _latest = (rgb, size)
                except Exception:
                    pass
    finally:
        sock.close()
        print("[✓] Cam: stream closed")


def get_latest() -> Optional[Tuple[bytes, Tuple[int, int]]]:
    with _frame_lock:
        return _latest
