import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_IMAGE = 'space.jpg'

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Background')

# Load and scale the background image
background = pygame.image.load(BACKGROUND_IMAGE)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()