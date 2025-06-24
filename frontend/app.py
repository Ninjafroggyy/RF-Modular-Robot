import pygame
import sys

from backend.network_communication.network import connect_to_robot, send_data


# ── Pygame setup ────────────────────────────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 1600, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Control Interface")
clock = pygame.time.Clock()          # controls the frame-rate

# ── Colours ─────────────────────────────────────────────────────────────────────
GREY   = (30, 30, 30)
RED    = (200, 0, 0)
YELLOW = (255, 215, 0)
GREEN  = (0, 200, 0)
BLUE   = (30, 144, 255)
DEFAULT_CIRCLE_COLOUR = (100, 100, 100)

# ── Circle state ────────────────────────────────────────────────────────────────
CIRCLE_RADIUS = 50
circle_x, circle_y = WIDTH // 2, HEIGHT // 2
current_circle_colour = DEFAULT_CIRCLE_COLOUR
MOVE_SPEED = 1                       # pixels per frame

ARROWS = {
    pygame.K_UP:    ("FORWARD", RED,    (0, -MOVE_SPEED)),
    pygame.K_DOWN:  ("BACKWARD", YELLOW,(0,  MOVE_SPEED)),
    pygame.K_LEFT:  ("LEFT",    BLUE,   (-MOVE_SPEED, 0)),
    pygame.K_RIGHT: ("RIGHT",   GREEN,  ( MOVE_SPEED, 0)),
}


def send_move(direction: str):
    """Fire a MOVE command to the Pi."""
    send_data({"command": "MOVE", "direction": direction})


def send_stop():
    """Tell the robot to stop moving."""
    send_data({"command": "STOP"})


def run_gui() -> None:
    """Main loop for the robot-control GUI with continuous motion."""
    global circle_x, circle_y, current_circle_colour

    #connect_to_robot()  # attempt connection once at start
    running = True
    while running:
        # ── Event handling ────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in ARROWS:
                    direction, colour, _ = ARROWS[event.key]
                    current_circle_colour = colour
                   # send_move(direction)           # <─ NEW
                elif event.key == pygame.K_SPACE:
                    current_circle_colour = DEFAULT_CIRCLE_COLOUR
                   # send_stop()                    # <─ NEW

            elif event.type == pygame.KEYUP:
                if event.key in ARROWS:
                    pass
                   # send_stop()                    # stop when arrow released

        # ── Continuous movement of the on-screen dot ─────────────────────────
        keys = pygame.key.get_pressed()
        for key, (_, _, delta) in ARROWS.items():
            if keys[key]:
                dx, dy = delta
                circle_x = max(CIRCLE_RADIUS, min(WIDTH  - CIRCLE_RADIUS, circle_x + dx))
                circle_y = max(CIRCLE_RADIUS, min(HEIGHT - CIRCLE_RADIUS, circle_y + dy))

        # ── Drawing ───────────────────────────────────────────────────────────
        screen.fill(GREY)
        pygame.draw.circle(screen, current_circle_colour,
                           (circle_x, circle_y), CIRCLE_RADIUS)
        pygame.display.flip()
        clock.tick(120)            # smooth 120 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_gui()
