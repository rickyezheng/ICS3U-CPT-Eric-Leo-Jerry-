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
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None

# Load images
# Map
map_image = pygame.image.load('assets/level.png').convert_alpha()
# Turret levels
turret_spritesheets= []
# For loop that cycles through the turret PNGS
for x in range(1, constants.TURRET_LEVELS + 1):
    turret_sheet = pygame.image.load(f'assets/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)

# Mouse cursor for turret
cursor_turret = pygame.image.load('assets/cursor_turret.png').convert_alpha()
# Dictionary for storing PNG in values
enemy_images = {
    "weak": pygame.image.load('assets/enemy_1.png').convert_alpha(),
    "medium": pygame.image.load('assets/enemy_2.png').convert_alpha(),
    "strong": pygame.image.load('assets/enemy_3.png').convert_alpha(),
    "elite": pygame.image.load('assets/enemy_4.png').convert_alpha()
}
# Buttons 
buy_turret_image = pygame.image.load('assets/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/cancel.png').convert_alpha()
upgrade_turret_image = pygame.image.load("assets/upgrade_turret.png").convert_alpha()
begin_image = pygame.image.load("assets/begin.png").convert_alpha()
restart_image = pygame.image.load("assets/restart.png").convert_alpha()
fast_forward_image = pygame.image.load("assets/fast_forward.png").convert_alpha()
# GUI
heart_image = pygame.image.load("assets/images/gui/heart.png").convert_alpha()
coin_image = pygame.image.load("assets/images/gui/coin.png").convert_alpha()
logo_image = pygame.image.load("assets/images/gui/logo.png").convert_alpha()

# Load sounds
shot_fx= pygame.mixer.Sound("assets/shot.wav")
shot_fx.set_volume(0.5)


# Load json data for level
with open('assets/level.tmj') as file:
    world_data = json.load(file)

# Fonts for text
text_font = pygame.font.SysFont("Consolas", 24, bold= True)
large_font = pygame.font.SysFont("Consolas", 36)

# Function for outputting the text       
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def display_data():
  #draw panel
  pygame.draw.rect(screen, "maroon", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
  pygame.draw.rect(screen, "grey0", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, 400), 2)
  screen.blit(logo_image, (constants.SCREEN_WIDTH, 400))
  #display data
  draw_text("LEVEL: " + str(world.level), text_font, "grey100", constants.SCREEN_WIDTH + 10, 10)
  screen.blit(heart_image, (constants.SCREEN_WIDTH + 10, 35))
  draw_text(str(world.health), text_font, "grey100", constants.SCREEN_WIDTH + 50, 40)
  screen.blit(coin_image, (constants.SCREEN_WIDTH + 10, 65))
  draw_text(str(world.money), text_font, "grey100", constants.SCREEN_WIDTH + 50, 70)

# Function for mouse position
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * constants.COLS) + mouse_tile_x
    # Check if tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free ==True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
        # Deduct cost of turret
        world.money-=constants.BUY_COST

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
        
        if game_over == False:
            #check if player has lost
            if world.health <= 0:
                game_over = True
                game_outcome = -1 #loss
            #check if player has won
            if world.level > constants.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1 #win
        
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

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
            
        # Displaying money and health
        draw_text(str(world.health), text_font, "grey100", 0, 0)
        draw_text(str(world.money), text_font, "grey100", 0, 30)
        draw_text(str(world.level), text_font, "grey100", 0, 60)

        if game_over == False:
            # Check if the level has been started or not
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                #fast forward option
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
        
        # Check if the wave is finished
        if world.check_level_complete() == True:
            world.money += constants.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level()
            world.process_enemies()

        # Draw buttons
        # Button for placing turrets
        # For the "turret button" show cost of turret and draw the button
        draw_text(str(constants.BUY_COST), text_font, "grey100", constants.SCREEN_WIDTH + 215, 135)
        screen.blit(coin_image, (constants.SCREEN_WIDTH + 260, 130))
        if turret_button.draw(screen):
            placing_turrets = True
        # If placing turrets then show the cancel button as well
        if placing_turrets==True:
            # Show cursor turret
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= constants.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
        # If a turret is selected then show the upgrade button
        if selected_turret:
            # If it can be upgraded show button
            if selected_turret.upgrade_level < constants.TURRET_LEVELS:
                draw_text(str(constants.UPGRADE_COST), text_font, "grey100", constants.SCREEN_WIDTH + 215, 195)
                screen.blit(coin_image, (constants.SCREEN_WIDTH + 260, 190))
                if upgrade_button.draw(screen):
                    if world.money >= constants.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= constants.UPGRADE_COST

    else:
        pygame.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("YOU WIN!", large_font, "grey0", 315, 230)
        # Restart level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pygame.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            # Empty groups
            enemy_group.empty()
            turret_group.empty()

    # Event handler (add comments)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if state == 'start' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets ==True:
                    # Check if there is enough money
                    if world.money >= constants.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)
        if state == 'exit':
            run = False

    pygame.display.flip()

pygame.quit()