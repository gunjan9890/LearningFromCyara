import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Seconds Hand")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Hand properties
hand_width, hand_length = 25, 100  # Width and length of the hand
angle = 0  # Starting angle
speed = 30  # Increase speed to create circular effect

# Center point of rotation
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Clock to control frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the end position of the hand
    end_x = center_x + hand_length * math.cos(math.radians(angle - 90))
    end_y = center_y + hand_length * math.sin(math.radians(angle - 90))

    # Draw the hand and accumulate drawings
    pygame.draw.line(screen, RED, (center_x, center_y), (end_x, end_y), hand_width)

    # Update the angle for the next frame
    angle = (angle + speed) % 360

    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
