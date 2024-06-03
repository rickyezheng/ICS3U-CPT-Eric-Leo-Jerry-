import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants
from main_menu import MainMenu
from settings import Settings

# Initialize pygame
pygame.init()

# Create clock
clock = pygame.time.Clock()

# Create game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence")

# Game variables
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None

# Load images
map_image = pygame.image.load('assets/level.png').convert_alpha()
#turret levels
turret_spritesheets= []
#for loop that cycles through the turret PNGS
for x in range(1, constants.TURRET_LEVELS + 1):
    turret_sheet = pygame.image.load(f'assets/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)


cursor_turret = pygame.image.load('assets/cursor_turret.png').convert_alpha()
enemy_images = {
    "weak": pygame.image.load('assets/enemy_1.png').convert_alpha(),
    "medium": pygame.image.load('assets/enemy_2.png').convert_alpha(),
    "strong": pygame.image.load('assets/enemy_3.png').convert_alpha(),
    "elite": pygame.image.load('assets/enemy_4.png').convert_alpha()
}
buy_turret_image = pygame.image.load('assets/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/cancel.png').convert_alpha()
upgrade_turret_image = pygame.image.load("assets/upgrade_turret.png").convert_alpha()



# Load json data for level
with open('assets/level.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * constants.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free ==True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
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

# Create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

# Create buttons
turret_button = Button(constants.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(constants.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(constants.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)

# Initialize main menu and settings
main_menu = MainMenu(screen)
settings = Settings(screen)
state = 'main_menu'

# Game loop
run = True
while run:
    clock.tick(constants.FPS)

    if state == 'main_menu':
        state = main_menu.draw()
    elif state == 'settings':
        state = settings.draw()
    elif state == 'start':
        #########################
        # UPDATING SECTION
        #########################

        enemy_group.update()
        turret_group.update(enemy_group)

        if selected_turret:
            selected_turret.selected = True

        #########################
        # DRAWING SECTION
        #########################

        screen.fill("grey100")
        world.draw(screen)
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        #spawn enemies
        if pygame.time.get_ticks() - last_enemy_spawn > constants.SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list):
                enemy_type = world.enemy_list[world.spawned_enemies]
                enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                enemy_group.add(enemy)
                world.spawned_enemies += 1
                last_enemy_spawn = pygame.time.get_ticks()

        if turret_button.draw(screen):
            placing_turrets = True
        if placing_turrets==True:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= constants.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
        if selected_turret:
            #if it can be upgraded show button
            if selected_turret.upgrade_level < constants.TURRET_LEVELS:
                if upgrade_button.draw(screen):
                    selected_turret.upgrade()

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
