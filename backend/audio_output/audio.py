""" Handles audio stream playback from the Pi microphone. """

import sounddevice as sd
import numpy as np


stream = None
AUDIO_SAMPLE_RATE = 44100  # Typical sample rate


def start_audio_stream():
    """ Start audio streaming from the Pi. """
    # This would be replaced by actual stream receiving from the Pi
    print("[INFO] Starting audio stream (not implemented yet).")


def stop_audio_stream():
    """ Stop audio streaming. """
    print("[INFO] Stopping audio stream.")


def play_audio_data(audio_data):
    """
    Play raw audio data received from the Pi.
    Args:
        audio_data (np.ndarray): PCM audio buffer
    """
    try:
        sd.play(audio_data, samplerate=AUDIO_SAMPLE_RATE)
    except Exception as e:
        print(f"[ERROR] Could not play audio: {e}")
