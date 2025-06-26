"""
Receive raw PCM audio from the Pi and play it via PyAudio.
"""

from __future__ import annotations

import socket
import threading
from typing import Optional

import pyaudio

from backend.config import HOST, AUDIO_PORT


class AudioReceiver:
    _CHUNK     = 1024
    _FORMAT    = pyaudio.paInt16
    _CHANNELS  = 2
    _RATE      = 44_100

    def __init__(self) -> None:
        self._sock: Optional[socket.socket] = None
        self._pyaudio = pyaudio.PyAudio()
        self._stream: Optional[pyaudio.Stream] = None
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None

    # ── Lifecycle ───────────────────────────────────────────────────
    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running.clear()
        if self._thread:
            self._thread.join()
        self._close()

    # ── Internals ───────────────────────────────────────────────────
    def _open(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((HOST, AUDIO_PORT))
        self._stream = self._pyaudio.open(
            format=self._FORMAT,
            channels=self._CHANNELS,
            rate=self._RATE,
            output=True,
            frames_per_buffer=self._CHUNK,
        )
        print(f"[✓] Audio: connected to {HOST}:{AUDIO_PORT}")

    def _close(self) -> None:
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._sock:
            self._sock.close()

    def _loop(self) -> None:
        try:
            self._open()
            while self._running.is_set():
                data = self._sock.recv(self._CHUNK)
                if not data:
                    break
                self._stream.write(data)
        except Exception as exc:
            print(f"[Audio] stream error: {exc}")
        finally:
            self._close()
            print("[✓] Audio: stream closed")
