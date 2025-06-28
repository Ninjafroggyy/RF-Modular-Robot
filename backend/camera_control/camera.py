"""
camera.py — MJPEG Stream Receiver for Camera Feed

Receives MJPEG frames over TCP from the Raspberry Pi’s camera server, decodes them into
raw RGB format, and stores the latest frame for retrieval by the GUI frontend.

"""

import io
import socket
import threading
from typing import Optional, Tuple

from PIL import Image

from backend.config import HOST, CAMERA_PORT

# ── Constants ──────────────────────────────────────────────────────────────
_BUFFER      = 4096                          # Socket buffer size
_JPEG_SOI    = b"\xff\xd8"                   # Start of JPEG image
_JPEG_EOI    = b"\xff\xd9"                   # End of JPEG image

# ── Shared state ───────────────────────────────────────────────────────────
_frame_lock  = threading.Lock()
_latest: Optional[Tuple[bytes, Tuple[int, int]]] = None  # (raw RGB bytes, (width, height))


def _decode(jpg_bytes: bytes) -> Tuple[bytes, Tuple[int, int]]:
    """
    Convert JPEG bytes to raw RGB bytes and return size.

    Args:
        jpg_bytes: A complete JPEG image in bytes.

    Returns:
        Tuple containing:
            - Raw RGB byte data
            - (width, height) of the image
    """
    img = Image.open(io.BytesIO(jpg_bytes)).convert("RGB")
    return img.tobytes(), img.size


def camera_stream_loop() -> None:
    """
    Continuously receive MJPEG frames from the camera server and store the latest one.

    Runs in a separate thread. Converts each complete JPEG frame to RGB bytes and
    stores it in a thread-safe global variable for real-time display by the frontend.
    """
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

            # Extract complete JPEG images from the stream buffer
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
                    pass  # Ignore corrupt or partial frames
    finally:
        sock.close()
        print("[✓] Cam: stream closed")


def get_latest() -> Optional[Tuple[bytes, Tuple[int, int]]]:
    """
    Return the most recently received RGB frame.

    Returns:
        A tuple (rgb_bytes, (width, height)), or None if no frame has been received yet.
    """
    with _frame_lock:
        return _latest
