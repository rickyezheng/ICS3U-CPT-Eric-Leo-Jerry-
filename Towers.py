import pygame

all_sprites = pygame.sprite.Group()
towers = pygame.sprite.Group()
enemies = pygame.sprite.Group()

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cost = 0
        self.attack_damage = 0
        self.attack_speed = 0
        self.attack_range = 0
        self.splash_damage = 0

    def shoot(self, enemies):
        for enemy in enemies:
            if enemy.rect.distance_to(self.rect) < self.attack_range:
                projectile = self.create_projectile(enemy)
                all_sprites.add(projectile)

    def create_projectile(self, target):
        pass

class CheapTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 255, 0))
        self.cost = 50
        self.attack_damage = 10
        self.attack_speed = 1000  # milliseconds
        self.attack_range = 200
        self.splash_damage = 5

    def create_projectile(self, target):
        return SplashProjectile(self.rect.centerx, self.rect.centery, target, self.attack_damage, self.splash_damage)

class ExpensiveTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((255, 0, 0))
        self.cost = 150
        self.attack_damage = 50
        self.attack_speed = 500  # milliseconds
        self.attack_range = 300

    def create_projectile(self, target):
        return FastProjectile(self.rect.centerx, self.rect.centery, target, self.attack_damage)

class SplashProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target, damage, splash_damage):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = target
        self.damage = damage
        self.splash_damage = splash_damage
        self.speed = 10

    def update(self):
        self.rect.x += (self.target.rect.x - self.rect.x) / self.speed
        self.rect.y += (self.target.rect.y - self.rect.y) / self.speed
        if self.rect.distance_to(self.target.rect) < 5:
            self.target.take_damage(self.damage)
            for enemy in enemies:
                if enemy.rect.distance_to(self.rect) < 50:
                    enemy.take_damage(self.splash_damage)
            self.kill()

class FastProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target, damage):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = target
        self.damage = damage
        self.speed = 20

    def update(self):
        self.rect.x += (self.target.rect.x - self.rect.x) / self.speed
        self.rect.y += (self.target.rect.y - self.rect.y) / self.speed
        if self.rect.distance_to(self.target.rect) < 5:
            self.target.take_damage(self.damage)
            self.kill()