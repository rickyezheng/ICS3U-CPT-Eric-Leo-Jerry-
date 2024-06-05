import pygame
import constants

class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)  # Adjust the font size as needed
        self.title = self.font.render("Settings", True, pygame.Color('White'))

        # Calculate positions for buttons
        screen_center_x = (constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2
        self.back_button = Button(screen_center_x, 400, "Back", self.font, (255, 255, 255), (100, 100, 100))

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        title_rect = self.title.get_rect(center=((constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2, 100))
        self.screen.blit(self.title, title_rect)
        if self.back_button.draw(self.screen):
            return 'main_menu'
        return 'settings'

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