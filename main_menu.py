import pygame
import constants

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = Button(constants.SCREEN_WIDTH // 2 - 100, 200, 'Start')
        self.exit_button = Button(constants.SCREEN_WIDTH // 2 - 100, 300, 'Exit')

    def draw(self):
        self.screen.fill("grey100")
        self.draw_text("Tower Defence", 50, constants.SCREEN_WIDTH // 2, 100)
        if self.start_button.draw(self.screen):
            return 'start'
        if self.exit_button.draw(self.screen):
            return 'exit'
        return 'main_menu'

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, "black")
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, x, y, text):
        self.image = pygame.Surface((200, 50))
        self.image.fill("darkgrey")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.text_surf = self.font.render(self.text, True, "black")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)
        return self.is_clicked()

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False
