import pygame
import sys
import constants

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 74)  # Adjust the font size as needed
        self.button_font = pygame.font.Font(None, 50)  # Adjust the font size as needed
        self.title = self.title_font.render("Tower Defence", True, pygame.Color('White'))

        # Calculate button positions to be centered based on the title's center
        screen_center_x = (constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2
        self.start_button = Button(screen_center_x, 200, "Start", self.button_font, (255, 255, 255), (100, 100, 100))
        self.exit_button = Button(screen_center_x, 300, "Exit", self.button_font, (255, 255, 255), (100, 100, 100))

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        title_rect = self.title.get_rect(center=((constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2, 100))
        self.screen.blit(self.title, title_rect)
        if self.start_button.draw(self.screen):
            return 'start'
        if self.exit_button.draw(self.screen):
            return 'exit'
        return 'main_menu'

class Button:
    def __init__(self, center_x, y, text, font, color, hover_color):
        self.image = font.render(text, True, color)
        self.hover_image = font.render(text, True, hover_color)
        self.rect = self.image.get_rect(center=(center_x, y))
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(self.hover_image, self.rect.topleft)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            screen.blit(self.image, self.rect.topleft)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action