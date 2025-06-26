import sys
import threading

import pygame

from backend.network_communication import network
from backend.audio_output.audio import AudioReceiver
from backend.camera_control.camera import camera_stream_loop, get_latest

# ── Pygame setup ─────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Control Interface")
clock = pygame.time.Clock()

# ── Colours ──────────────────────────────────────────
GREY   = (30, 30, 30)
RED    = (200, 0, 0)
YELLOW = (255, 215, 0)
GREEN  = (0, 200, 0)
BLUE   = (30, 144, 255)
DEFAULT = (100, 100, 100)

# ── Circle state ─────────────────────────────────────
RADIUS = 50
x, y   = WIDTH // 2, HEIGHT // 2
colour = DEFAULT
SPEED  = 1

ARROWS = {
    pygame.K_UP:    ("forward",  RED,    (0, -SPEED)),
    pygame.K_DOWN:  ("backward", YELLOW, (0,  SPEED)),
    pygame.K_LEFT:  ("left",     BLUE,   (-SPEED, 0)),
    pygame.K_RIGHT: ("right",    GREEN,  ( SPEED, 0)),
}


def run_gui() -> None:
    global x, y, colour

    network.connect()

    # Start backend streams
    audio = AudioReceiver()
    audio.start()
    threading.Thread(target=camera_stream_loop, daemon=True).start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in ARROWS:
                    dir_, colour, _ = ARROWS[event.key]
                    network.send({"type": "movement", "direction": dir_})
                elif event.key == pygame.K_SPACE:
                    network.send({"type": "movement", "direction": "stop"})
            elif event.type == pygame.KEYUP:
                if event.key in ARROWS:
                    network.send({"type": "movement", "direction": "stop"})

        # continuous local circle update
        keys = pygame.key.get_pressed()
        for key, (_, _, delta) in ARROWS.items():
            if keys[key]:
                dx, dy = delta
                x = max(RADIUS, min(WIDTH  - RADIUS, x + dx))
                y = max(RADIUS, min(HEIGHT - RADIUS, y + dy))

        # ── Drawing ───────────────────────────────────
        screen.fill(GREY)

        # Camera
        frame = get_latest()
        if frame:
            rgb, (w, h) = frame
            surf = pygame.image.frombuffer(rgb, (w, h), "RGB")
            screen.blit(surf, (20, 20))

        # Circle
        pygame.draw.circle(screen, colour, (x, y), RADIUS)
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    audio.stop()
    network.disconnect()
    sys.exit()
