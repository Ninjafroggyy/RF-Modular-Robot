"""
Central network configuration shared by all backend modules.
Edit here only; every other file simply does `from backend.config import HOST, *`.
"""
HOST          = "192.168.77.2"  # Raspberry Pi IP
CTRL_PORT     = 5000            # JSON command channel (network.py)
AUDIO_PORT    = 5001            # Raw PCM audio
CAMERA_PORT   = 5002            # MJPEG stream
