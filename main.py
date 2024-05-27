import pygame
from enemy import Enemy
import constants

#initialise pygame
pygame.init()

#create clock
clock = pygame.time.Clock()

#create game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence")

#load images
enemy_image = pygame.image.load('assets/enemy_1.png').convert_alpha()

#create groups
enemy_group = pygame.sprite.Group()

enemy = Enemy((200, 300), enemy_image)
enemy_group.add(enemy)

#game loop
run = True
while run:

  clock.tick(constants.FPS)

  screen.fill("grey100")

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)

  #event handler
  for event in pygame.event.get():
    #quit program
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.flip()

pygame.quit()