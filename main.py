import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Basic classes
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 10
        self.attack_speed = 1  # Attacks per second

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 20)

    def attack(self, enemies):
        for enemy in enemies:
            if self.in_range(enemy):
                enemy.health -= self.damage

    def in_range(self, enemy):
        return ((self.x - enemy.x)**2 + (self.y - enemy.y)**2) ** 0.5 <= self.range

class Enemy:
    def __init__(self, path):
        self.path = path
        self.x, self.y = self.path[0]
        self.speed = 2
        self.health = 100
        self.path_index = 0

    def update(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            direction_x = target_x - self.x
            direction_y = target_y - self.y
            distance = (direction_x**2 + direction_y**2) ** 0.5

            if distance <= self.speed:
                self.path_index += 1
                self.x, self.y = target_x, target_y
            else:
                self.x += self.speed * direction_x / distance
                self.y += self.speed * direction_y / distance

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 20, 20))

# Main game loop
clock = pygame.time.Clock()
towers = [Tower(200, 300)]
enemies = [Enemy([(100, 100), (200, 200), (300, 300), (400, 400)])]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update game state
    for enemy in enemies:
        enemy.update()

    for tower in towers:
        tower.attack(enemies)

    # Draw everything
    screen.fill(WHITE)
    for tower in towers:
        tower.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)
