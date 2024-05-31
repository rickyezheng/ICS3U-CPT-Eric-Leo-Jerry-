import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants
from main_menu import MainMenu

#initialise pygame
pygame.init()

#create clock
clock = pygame.time.Clock()

#create game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence")

#game variables
placing_turrets = False
selected_turret = None

#load images
#map
map_image = pygame.image.load('assets/level.png').convert_alpha()
#turret spritesheets
turret_sheet = pygame.image.load('assets/turret_1.png').convert_alpha()
#individual turret image for mouse cursor
cursor_turret = pygame.image.load('assets/cursor_turret.png').convert_alpha()
#enemies
enemy_image = pygame.image.load('assets/enemy_1.png').convert_alpha()
#buttons
buy_turret_image = pygame.image.load('assets/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/cancel.png').convert_alpha()
upgrade_turret_image=pygame.image.load("assets/upgrade_turret.png").convert_alpha()
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
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#create buttons
turret_button = Button(constants.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(constants.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(constants.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)

#initialize main menu
main_menu = MainMenu(screen)
state = 'main_menu'

#game loop
run = True
while run:
    clock.tick(constants.FPS)

    if state == 'main_menu':
        state = main_menu.draw()
    elif state == 'start':
        #########################
        # UPDATING SECTION
        #########################

        #update groups
        enemy_group.update()
        turret_group.update(enemy_group)

        #highlight selected turret
        if selected_turret:
            selected_turret.selected = True

        #########################
        # DRAWING SECTION
        #########################

        screen.fill("grey100")

        #draw level
        world.draw(screen)

        #draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        #draw buttons
        if turret_button.draw(screen):
            placing_turrets = True
        if placing_turrets == True:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= constants.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
    #if turret has been selected, show upgrade
    if selected_turret:
        if upgrade_button.draw(screen):
            selected_turret.upgrade()
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if state == 'start' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)
        if state == 'exit':
            run = False

    pygame.display.flip()

pygame.quit()
