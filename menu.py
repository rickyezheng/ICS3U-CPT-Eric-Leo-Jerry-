import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WYZ Tower Defence")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for title
TITLE_FONT_SIZE = 64
TITLE_FONT_COLOR = WHITE
title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE)

# Menu settings
MENU_FONT_SIZE = 32
MENU_FONT_COLOR = WHITE
MENU_BACKGROUND_COLOR = BLACK
MENU_OPTIONS = ["Start Game", "Quit"]

def draw_menu(screen, menu_options, font_size, font_color, background_color):
    """Draws the menu on the screen."""
    font = pygame.font.SysFont(None, font_size)
    y = SCREEN_HEIGHT // 2
    for option in menu_options:
        text = font.render(option, True, font_color, background_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(text, text_rect)
        y += font_size * 2

def main_menu():
    """Displays the main menu and waits for user input."""
    screen.fill(MENU_BACKGROUND_COLOR)
    title_text = title_font.render("WYZ Tower Defence", True, TITLE_FONT_COLOR)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    draw_menu(screen, MENU_OPTIONS, MENU_FONT_SIZE, MENU_FONT_COLOR, MENU_BACKGROUND_COLOR)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < SCREEN_HEIGHT // 2 + MENU_FONT_SIZE * 2:
                    # Start game
                    print("Starting game...")
                    game_loop()
                elif y > SCREEN_HEIGHT // 2 + MENU_FONT_SIZE * 2 and y < SCREEN_HEIGHT // 2 + MENU_FONT_SIZE * 4:
                    # Quit game
                    print("Quitting game...")
                    pygame.quit()
                    sys.exit()

def game_loop():
    """The main game loop."""
    # Initialize game state here
    #...

    # Main game loop
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game state here
        #...

        # Draw everything
        screen.fill(WHITE)
        # Draw game objects here
        #...

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()