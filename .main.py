import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
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
#individual turret image for mouse cursor
cursor_turret = pygame.image.load('assets/cursor_turret.png').convert_alpha()
#enemies
enemy_image = pygame.image.load('assets/enemy_1.png').convert_alpha()

#load json data for level
with open('assets/level.tmj') as file:
  world_data = json.load(file)

def create_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * constants.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] == 7:
    #check that there isn't already a turret there
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
    #if it is a free space then create turret
    if space_is_free == True:
      new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
      turret_group.add(new_turret)

#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

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
  turret_group.draw(screen)

  #event handler
  for event in pygame.event.get():
    #quit program
    if event.type == pygame.QUIT:
      run = False
    #mouse click
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pygame.mouse.get_pos()
      #check if mouse is on the game area
      if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
        create_turret(mouse_pos)

  #update display
  pygame.display.flip()

pygame.quit()