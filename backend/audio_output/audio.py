"""
audio.py — Live PCM Audio Receiver for Robot Stream

Receives raw PCM audio data over TCP from the Raspberry Pi and plays it in real time
using PyAudio.

"""

from __future__ import annotations

import socket
import threading
from typing import Optional

import pyaudio

from backend.config import HOST, AUDIO_PORT


class AudioReceiver:
    """
    Handles real-time audio streaming from a remote source.

    Establishes a TCP connection to the Raspberry Pi audio server,
    receives raw PCM data, and plays it through the system audio output.

    Audio Format:
        - PCM 16-bit, stereo (2 channels)
        - 44.1 kHz sample rate
    """

    _CHUNK     = 1024
    _FORMAT    = pyaudio.paInt16
    _CHANNELS  = 2
    _RATE      = 44_100

    def __init__(self) -> None:
        """Initialise the audio receiver and prepare for streaming."""
        self._sock: Optional[socket.socket] = None
        self._pyaudio = pyaudio.PyAudio()
        self._stream: Optional[pyaudio.Stream] = None
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None

    # ── Lifecycle ───────────────────────────────────────────────────
    def start(self) -> None:
        """
        Start the audio receiver in a background thread.

        If already running, this has no effect.
        """
        if self._thread and self._thread.is_alive():
            return
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the audio receiver and clean up resources.
        """
        self._running.clear()
        if self._thread:
            self._thread.join()
        self._close()

    # ── Internals ───────────────────────────────────────────────────
    def _open(self) -> None:
        """Open the TCP connection and initialise the PyAudio stream."""
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
        """Close the audio stream and socket connection."""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._sock:
            self._sock.close()

    def _loop(self) -> None:
        """Main audio receiving loop."""
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
