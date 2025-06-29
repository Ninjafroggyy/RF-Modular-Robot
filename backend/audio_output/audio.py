""" Receives raw audio data over TCP from the Raspberry Pi and plays it in real time using PyAudio. """
# Library imports
from __future__ import annotations
from typing import Optional
import socket
import threading
import pyaudio
# Program file imports
from backend.config import HOST, AUDIO_PORT


class AudioReceiver:
    """
        Handles real-time audio streaming from a remote source. Establishes a TCP connection to the Raspberry Pi
        audio server, receives raw PCM data, and plays it through the system audio output.
    """
    _CHUNK     = 1024
    _FORMAT    = pyaudio.paInt16
    _CHANNELS  = 2
    _RATE      = 44_100

    def __init__(self):
        """Initialise the audio receiver and prepare for streaming."""
        self._sock: Optional[socket.socket] = None
        self._pyaudio = pyaudio.PyAudio()
        self._stream: Optional[pyaudio.Stream] = None
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._active = False  # Track true running state for GUI status

    def start(self):
        """ Start the audio receiver in a background thread. """
        if self._thread and self._thread.is_alive():
            return
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        """ Stop the audio receiver and clean up resources. """
        self._running.clear()
        if self._thread:
            self._thread.join()
        self._close()
        self._active = False  # Mark as inactive

    def is_running(self):
        """ Return True if the audio receiver is currently active. """
        return self._active

    def _open(self):
        """ Open the TCP connection and initialise the PyAudio stream."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((HOST, AUDIO_PORT))
        self._stream = self._pyaudio.open(
            format=self._FORMAT,
            channels=self._CHANNELS,
            rate=self._RATE,
            output=True,
            frames_per_buffer=self._CHUNK,
        )
        self._active = True  # Set to active once audio starts
        print(f"AUDIO: connected to {HOST}:{AUDIO_PORT}")

    def _close(self):
        """ Close the audio stream and socket connection."""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._sock:
            self._sock.close()
            self._sock = None

    def _loop(self):
        """ Main audio receiving loop."""
        try:
            self._open()
            while self._running.is_set():
                data = self._sock.recv(self._CHUNK)
                if not data:
                    break
                self._stream.write(data)
        except Exception as exc:
            print(f"AUDIO stream error: {exc}")
        finally:
            self._close()
            self._active = False  # Ensure active state is cleared on disconnect
            print("AUDIO: stream closed")
