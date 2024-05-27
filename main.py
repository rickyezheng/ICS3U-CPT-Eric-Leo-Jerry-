import pygame
import json
from enemy import Enemy
from world import World
import constants

#initialise pygame
pygame.init()

#create clock
clock = pygame.time.Clock()

#create game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence")

#load images
#map
map_image = pygame.image.load('assets/level.png').convert_alpha()
#enemies
enemy_image = pygame.image.load('assets/enemy_1.png').convert_alpha()

#load json data for level
with open('assets/level.tmj') as file:
  world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pygame.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#game loop
run = True
while run:

  clock.tick(constants.FPS)

  screen.fill("grey100")

  #draw level
  world.draw(screen)

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