"""
app.py — Main GUI Interface for Robot Control

This script initialises and runs the Pygame-based control interface for the robot.
It handles keyboard input to control movement, displays visual feedback on screen,
and sends commands over the network to the Raspberry Pi robot system.

"""

import sys
import threading
import pygame

from backend.network_communication import network
from backend.audio_output.audio import AudioReceiver
from backend.camera_control.camera import camera_stream_loop, get_latest

# ─── Pygame Setup ───────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Control Interface")
clock = pygame.time.Clock()

# ─── Colour Definitions ─────────────────────────────────
GREY    = (30, 30, 30)
RED     = (200, 0, 0)
YELLOW  = (255, 215, 0)
GREEN   = (0, 200, 0)
BLUE    = (30, 144, 255)
DEFAULT = (100, 100, 100)

# ─── Circle State ───────────────────────────────────────
RADIUS = 50
x, y   = WIDTH // 2, HEIGHT // 2
colour = DEFAULT
SPEED  = 1

# ─── Movement Mapping ───────────────────────────────────
ARROWS = {
    pygame.K_UP:    ("forward",  RED,    (0, -SPEED)),
    pygame.K_DOWN:  ("backward", YELLOW, (0,  SPEED)),
    pygame.K_LEFT:  ("left",     BLUE,   (-SPEED, 0)),
    pygame.K_RIGHT: ("right",    GREEN,  ( SPEED, 0)),
}


def run_gui() -> None:
    """
    Runs the main GUI loop for robot control.
    Initialises network and audio streams, listens for key input to
    control robot movement, and displays camera feed and motion status.
    """
    global x, y, colour

    # Connect to robot
    network.connect()

    # Start audio receiver and camera stream in separate threads
    audio = AudioReceiver()
    audio.start()
    threading.Thread(target=camera_stream_loop, daemon=True).start()

    running = True
    keys_pressed = set()  # Track currently held keys

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in ARROWS:
                    dir_, colour, _ = ARROWS[event.key]
                    keys_pressed.add(event.key)
                    network.send({"type": "movement", "direction": dir_})
                    print(f"[SENT] Movement: {dir_}")  # Local debug print
                elif event.key == pygame.K_SPACE:
                    network.send({"type": "movement", "direction": "stop"})
                    print(f"[SENT] Movement: stop")  # Local debug print

            elif event.type == pygame.KEYUP:
                if event.key in ARROWS:
                    keys_pressed.discard(event.key)
                    network.send({"type": "movement", "direction": "stop"})
                    print(f"[SENT] Movement: stop")  # Local debug print

        # Determine if no arrow keys are currently pressed
        if not keys_pressed:
            colour = DEFAULT  # Reset to default colour if no movement

        # Update circle position continuously if key held
        keys = pygame.key.get_pressed()
        for key, (_, _, delta) in ARROWS.items():
            if keys[key]:
                dx, dy = delta
                x = max(RADIUS, min(WIDTH  - RADIUS, x + dx))
                y = max(RADIUS, min(HEIGHT - RADIUS, y + dy))

        # ─── Drawing Section ─────────────────────────────
        screen.fill(GREY)

        # Display camera frame if available
        frame = get_latest()
        if frame:
            rgb, (w, h) = frame
            surf = pygame.image.frombuffer(rgb, (w, h), "RGB")
            screen.blit(surf, (20, 20))

        # Draw circle at current position
        pygame.draw.circle(screen, colour, (x, y), RADIUS)

        pygame.display.flip()
        clock.tick(120)

    # ─── Clean Shutdown ────────────────────────────────
    pygame.quit()
    audio.stop()
    network.disconnect()
    sys.exit()
