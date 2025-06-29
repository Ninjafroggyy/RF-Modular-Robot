""" Defines the Raspberry Pi IP address and the ports used for each communication channel. """
# ── IP Address ─────────────────────────────────────────────────────
# Temporary dual-host setup for switching between locations
HOST = "192.168.77.2"    # Raspberry Pi IP (mobile hotspot)
# HOST = "192.168.0.13"      # Raspberry Pi IP (home network)

# ── Port Assignments ───────────────────────────────────────────────
CTRL_PORT   = 5000  # Control commands (JSON)
AUDIO_PORT  = 5001  # Raw PCM audio stream
CAMERA_PORT = 5002  # MJPEG video stream
