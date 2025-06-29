"""
    This script initialises and runs the control interface for the robot. It handles keyboard input to control movement,
    displays visual feedback on screen, displays a live camera feed, and shows microphone connection status.
"""
# Library imports
import sys
import threading
import pygame
# Program file imports
from backend.network_communication import network
from backend.audio_output.audio import AudioReceiver
from backend.camera_control.camera import camera_stream_loop, get_latest

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Control Interface")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colour Definitions
GREY    = (30, 30, 30)
DARK    = (20, 20, 20)
RED     = (200, 0, 0)
YELLOW  = (255, 215, 0)
GREEN   = (0, 200, 0)
BLUE    = (30, 144, 255)
DEFAULT = (100, 100, 100)

# Circle State
RADIUS = 25
x, y   = 350, HEIGHT // 2  # Centered in left panel
colour = DEFAULT
SPEED  = 1

# Movement Mapping
ARROWS = {
    pygame.K_UP:    ("forward",  RED,    (0, -SPEED)),
    pygame.K_DOWN:  ("backward", YELLOW, (0,  SPEED)),
    pygame.K_LEFT:  ("left",     BLUE,   (-SPEED, 0)),
    pygame.K_RIGHT: ("right",    GREEN,  ( SPEED, 0)),
}


def run_gui():
    """
        Runs the main GUI loop for robot control. Connects to the robot and audio stream, handles movement input,
        displays a split-screen UI with camera feed and mic status.
    """
    global x, y, colour

    # Connect to robot
    network.connect()

    # Start audio and camera threads
    audio = AudioReceiver()
    audio.start()
    threading.Thread(target=camera_stream_loop, daemon=True).start()

    running = True
    keys_pressed = set()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in ARROWS:
                    dir_, colour, _ = ARROWS[event.key]
                    keys_pressed.add(event.key)
                    network.send({"type": "movement", "direction": dir_})
                    print(f"[SENT] Movement: {dir_}")
                elif event.key == pygame.K_SPACE:
                    network.send({"type": "movement", "direction": "stop"})
                    print(f"[SENT] Movement: stop")

            elif event.type == pygame.KEYUP:
                if event.key in ARROWS:
                    keys_pressed.discard(event.key)
                    network.send({"type": "movement", "direction": "stop"})
                    print(f"[SENT] Movement: stop")

        # Update position if movement keys held
        keys = pygame.key.get_pressed()
        for key, (_, _, delta) in ARROWS.items():
            if keys[key]:
                dx, dy = delta
                x = max(RADIUS, min(700 - RADIUS, x + dx))
                y = max(RADIUS, min(HEIGHT - RADIUS, y + dy))

        if not keys_pressed:
            colour = DEFAULT

        # Drawing Section
        screen.fill(GREY)

        # Left panel: Movement zone
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 700, HEIGHT))
        pygame.draw.circle(screen, colour, (x, y), RADIUS)

        # Right panel: Camera feed
        pygame.draw.rect(screen, DARK, (700, 0, 700, HEIGHT))
        frame = get_latest()
        if frame:
            rgb, (w, h) = frame
            cam_surf = pygame.image.frombuffer(rgb, (w, h), "RGB")
            cam_surf = pygame.transform.scale(cam_surf, (660, 500))
            screen.blit(cam_surf, (720, 40))

        # Mic status (top-right)
        mic_status = "MIC: ON" if audio.is_running() else "MIC: OFF"
        mic_color = GREEN if audio.is_running() else RED
        mic_text = font.render(mic_status, True, mic_color)
        screen.blit(mic_text, (WIDTH - 180, 20))

        pygame.display.flip()
        clock.tick(60)

    # Clean Shutdown when clicking X on the GUI
    pygame.quit()
    audio.stop()
    network.disconnect()
    sys.exit()
