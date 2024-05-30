import pygame

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tower Defence")

# Load images
title_image = pygame.image.load('assets/title.png').convert_alpha()
start_image = pygame.image.load('assets/start.png').convert_alpha()
exit_image = pygame.image.load('assets/exit.png').convert_alpha()

# Create buttons
start_button = start_image
start_button_rect = start_button.get_rect()
start_button_rect.x = 350
start_button_rect.y = 250

exit_button = exit_image
exit_button_rect = exit_button.get_rect()
exit_button_rect.x = 350
exit_button_rect.y = 350

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(pos):
                # Start the game
                run = False
                # Add your game code here
                #...
            if exit_button_rect.collidepoint(pos):
                run = False

    # Draw menu
    screen.fill("black")
    screen.blit(title_image, (250, 100))
    screen.blit(start_button, start_button_rect)
    screen.blit(exit_button, exit_button_rect)

    # Update display
    pygame.display.flip()

pygame.quit()