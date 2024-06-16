import pygame
import constants
import json
from button import Button

# Load settings from JSON file (Credit to Sonia for helping us figure out json files)
with open('setting.json', 'r') as f:
    settings = json.load(f)

class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.title = self.font.render("Settings", True, pygame.Color('White'))

        # Load settings
        self.volume = settings.get('volume')
        self.speed = settings.get('speed')

        # Create buttons so the user can increase or decrease volume and speed
        screen_center_x = (constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2
        self.back_button = Button(screen_center_x - 200, 500, pygame.image.load("assets/back.png").convert_alpha(), True)
        
        self.volume_up_button = Button(screen_center_x + 150, 200, pygame.image.load("assets/plus.png").convert_alpha(), True)
        self.volume_down_button = Button(screen_center_x - 150, 200, pygame.image.load("assets/minus.png").convert_alpha(), True)
        
        self.speed_up_button = Button(screen_center_x + 150, 300, pygame.image.load("assets/plus.png").convert_alpha(), True)
        self.speed_down_button = Button(screen_center_x - 150, 300, pygame.image.load("assets/minus.png").convert_alpha(), True)

        self.volume_label = self.font.render(f"Volume: {self.volume}", True, pygame.Color('White'))
        self.speed_label = self.font.render(f"Speed: {self.speed}", True, pygame.Color('White'))

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        title_rect = self.title.get_rect(center=((constants.SCREEN_WIDTH + constants.SIDE_PANEL) // 2, 100))
        self.screen.blit(self.title, title_rect)

        # Draw volume controls
        self.screen.blit(self.volume_label, (self.volume_down_button.rect.x + 95, self.volume_down_button.rect.y))
        if self.volume_up_button.draw(self.screen):
            self.volume = min(self.volume + 1, 10)  # Max volume 10
        if self.volume_down_button.draw(self.screen):
            self.volume = max(self.volume - 1, 0)  # Min volume 0
        self.volume_label = self.font.render(f"Volume: {self.volume}", True, pygame.Color('White'))

        # Draw speed controls
        self.screen.blit(self.speed_label, (self.speed_down_button.rect.x + 97, self.speed_down_button.rect.y))
        if self.speed_up_button.draw(self.screen):
            self.speed = min(self.speed + 1, 10)  # Max speed 10
        if self.speed_down_button.draw(self.screen):
            self.speed = max(self.speed - 1, 1)  # Min speed 1
        self.speed_label = self.font.render(f"Speed: {self.speed}", True, pygame.Color('White'))

        # Draw back button
        if self.back_button.draw(self.screen):
            self.save_settings()
            return 'main_menu'

        return 'settings'

    def save_settings(self):
        # Save settings to JSON file
        settings_data = {
            'volume': self.volume,
            'speed': self.speed
        }
        with open('setting.json', 'w') as file:
            json.dump(settings_data, file)
