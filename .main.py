import pygame
import json
import constants
#import Classes from other files
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from main_menu import MainMenu
from settings import Settings

# Initialize pygame
pygame.init()

# Create clock
clock = pygame.time.Clock()

# Create game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence")

# Load images
map_image = pygame.image.load('assets/level.png').convert_alpha()
turret_spritesheets = [pygame.image.load(f'assets/turret_{x}.png').convert_alpha() for x in range(1, constants.TURRET_LEVELS + 1)]
cursor_turret = pygame.image.load('assets/cursor_turret.png').convert_alpha()
enemy_images = {name: pygame.image.load(f'assets/enemy_{i}.png').convert_alpha() for i, name in enumerate(['weak', 'medium', 'strong', 'elite'], 1)}
buy_turret_image = pygame.image.load('assets/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/cancel.png').convert_alpha()
upgrade_turret_image = pygame.image.load("assets/upgrade_turret.png").convert_alpha()
begin_image = pygame.image.load("assets/begin.png").convert_alpha()
restart_image = pygame.image.load("assets/restart.png").convert_alpha()
fast_forward_image = pygame.image.load("assets/fast_forward.png").convert_alpha()
pause_image = pygame.image.load("assets/pause_1.png").convert_alpha()
exit_image = pygame.image.load("assets/exit.png").convert_alpha()
heart_image = pygame.image.load("assets/heart.png").convert_alpha()
coin_image = pygame.image.load("assets/coin.png").convert_alpha()
logo_image = pygame.image.load("assets/logo.png").convert_alpha()

# Load sounds
shot_fx = pygame.mixer.Sound("assets/shot.wav")
shot_fx.set_volume(0.5)

# Load json data for level
with open('assets/level.tmj') as file:
    world_data = json.load(file)

# Fonts for text
text_font = pygame.font.SysFont("Consolas", 24, bold=True)
large_font = pygame.font.SysFont("Consolas", 36)

# Function for outputting the text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    pygame.draw.rect(screen, "maroon", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
    pygame.draw.rect(screen, "grey0", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, 400), 2)
    screen.blit(logo_image, (constants.SCREEN_WIDTH, 400))
    draw_text("LEVEL: " + str(world.level), text_font, "grey100", constants.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (constants.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", constants.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_image, (constants.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", constants.SCREEN_WIDTH + 50, 70)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * constants.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            world.money -= constants.BUY_COST

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

# Create buttons (True = single click, False = click + hold)
turret_button = Button(constants.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(constants.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(constants.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(constants.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(constants.SCREEN_WIDTH + 50, 300, fast_forward_image, False)
pause_button = Button(constants.SCREEN_WIDTH + 225, 25, pause_image, True)
exit_button = Button(constants.SCREEN_WIDTH + 250, constants.SCREEN_HEIGHT//2, exit_image,True)

# Initialize main menu and settings
main_menu = MainMenu(screen)
settings = Settings(screen)
state = 'main_menu'

# Game variables
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None
paused = False

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

        if game_over == False:
            # Check if player has lost
            if world.health <= 0:
                game_over = True
                game_outcome = -1 # loss
            # Check if player has won
            if world.level >= constants.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1 # win

        if not paused:
            enemy_group.update(world)
            turret_group.update(enemy_group, world)

            if selected_turret:
                selected_turret.selected = True

        #########################
        # DRAWING SECTION
        #########################

        # Draw level
        world.draw(screen)
        # Draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        display_data()

        if game_over == False:
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                if not paused:
                    # Fast forward option
                    world.game_speed = 1
                    if fast_forward_button.draw(screen):
                        world.game_speed = 2
                    # Spawn enemies
                    if pygame.time.get_ticks() - last_enemy_spawn > constants.SPAWN_COOLDOWN:
                        if world.spawned_enemies < len(world.enemy_list):
                            enemy_type = world.enemy_list[world.spawned_enemies]
                            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                            enemy_group.add(enemy)
                            world.spawned_enemies += 1
                            last_enemy_spawn = pygame.time.get_ticks()
                else:
                    world.game_speed = 0

            # Handle the pause button click
            if pause_button.draw(screen):
                paused = not paused
                world.game_speed = 0 if paused else 1

            if paused:
                # Draw the exit button when paused
                if exit_button.draw(screen):
                    run = False

            # Check if the wave is finished
            if world.check_level_complete() == True:
                world.money += constants.LEVEL_COMPLETE_REWARD
                world.level += 1
                level_started = False
                last_enemy_spawn = pygame.time.get_ticks()
                world.reset_level()
                world.process_enemies()

            # Draw buttons
            if not paused:
                draw_text(str(constants.BUY_COST), text_font, "grey100", constants.SCREEN_WIDTH + 215, 135)
                screen.blit(coin_image, (constants.SCREEN_WIDTH + 260, 130))
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
                if selected_turret:
                    # if a turret can be upgraded then show the upgrade button
                    if selected_turret.upgrade_level < constants.TURRET_LEVELS:
                        # show cost of upgrade and draw the button
                        draw_text(str(constants.UPGRADE_COST), text_font, "grey100", constants.SCREEN_WIDTH + 215, 195)
                        screen.blit(coin_image, (constants.SCREEN_WIDTH + 260, 190))
                        if upgrade_button.draw(screen):
                            if world.money >= constants.UPGRADE_COST:
                                selected_turret.upgrade()
                                world.money -= constants.UPGRADE_COST

        else:
            pygame.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
            if game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("YOU WIN!", large_font, "grey0", 315, 230)
            if restart_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                enemy_group.empty()
                turret_group.empty()

    # Event handler (add comments)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if state == 'start' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                if not paused:
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        if world.money >= constants.BUY_COST:
                            create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)
        if state == 'exit':
            run = False

    pygame.display.flip()

pygame.quit()
