import pygame
import sys

# Initialise pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Control Interface")

# Define colors
WHITE = (255, 255, 255)
GREY = (30, 30, 30)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
GREEN = (0, 200, 0)
BLUE = (30, 144, 255)
DEFAULT_CIRCLE_COLOUR = (100, 100, 100)

# Circle position and size
CIRCLE_RADIUS = 50
CIRCLE_POS = (WIDTH // 2, HEIGHT // 2)

# Circle colour state
current_circle_colour = DEFAULT_CIRCLE_COLOUR


def handle_keydown(event):
    """Handle movement key presses and update circle colour."""
    global current_circle_colour

    if event.key == pygame.K_UP:
        print("Move Forward")
        current_circle_colour = RED
    elif event.key == pygame.K_DOWN:
        print("Move Backward")
        current_circle_colour = YELLOW
    elif event.key == pygame.K_LEFT:
        print("Turn Left")
        current_circle_colour = BLUE
    elif event.key == pygame.K_RIGHT:
        print("Turn Right")
        current_circle_colour = GREEN
    elif event.key == pygame.K_SPACE:
        print("Stop")
        current_circle_colour = DEFAULT_CIRCLE_COLOUR


def run_gui():
    """Main GUI loop for the robot control app."""
    global current_circle_colour

    running = True
    while running:
        screen.fill(GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event)

        # Draw the central circle
        pygame.draw.circle(screen, current_circle_colour, CIRCLE_POS, CIRCLE_RADIUS)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
