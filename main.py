# Libraries
import time
import pygame
from pygame import mixer
import csv

# Files
import variables
mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('getting_through_it')


# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.8
SCROLL_THRESH = 300
ROWS = 19
COLS = 32
TILE_SIZE = 32
TILE_TYPES = 180
MAX_LEVELS = 10

# Level variables
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
end_game = False
start_intro = True

# Defined player action variable
moving_left = False
moving_right = False

# Load music and sounds
# Music Handling:
menu_music_playing = False
levels_1to5_music_playing = False

jump_sound = pygame.mixer.Sound('assets/audio/sounds/jump_sound.ogg')
jump_sound.set_volume(0.4)
level_complete_sound = pygame.mixer.Sound(
    'assets/audio/sounds/level_complete_sound.ogg')
level_complete_sound.set_volume(0.15)
death_sound = pygame.mixer.Sound('assets/audio/sounds/death_sound.wav')
death_sound.set_volume(0.4)

# Load background images
level_1_img = pygame.image.load(f'assets/world/backgrounds/04.png')

# Load menu images
start_btn_sheet = pygame.image.load(
    f'assets/menu/start_btn.png').convert_alpha()
start_btn_UP = start_btn_sheet.subsurface(variables.btn_UP)
start_btn_DOWN = start_btn_sheet.subsurface(variables.btn_DOWN)

exit_btn_sheet = pygame.image.load(
    f'assets/menu/exit_btn.png').convert_alpha()
exit_btn_UP = exit_btn_sheet.subsurface(variables.btn_UP)
exit_btn_DOWN = exit_btn_sheet.subsurface(variables.btn_DOWN)

restart_btn_sheet = pygame.image.load(
    f'assets/menu/restart_btn.png').convert_alpha()
restart_btn_UP = restart_btn_sheet.subsurface(variables.btn_UP)
restart_btn_DOWN = restart_btn_sheet.subsurface(variables.btn_DOWN)

# Load tile images, store tiles in a list
tile_img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/world/Tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    if x == 130 or x == 156:
        img.set_alpha(0)
    if x == 37:
        img = pygame.transform.rotate(img, 180)
    tile_img_list.append(img)


# Define colors
BG = (0, 0, 0)
RED = (255, 0, 0)
PINK = (235, 65, 54)


def draw_bg():
    screen.fill(BG)
    screen.blit(level_1_img, (0, 0))


def reset_level():
    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Button():

    def __init__(self, x, y, image, image_pressed, scale):
        width = image.get_width()
        height = image.get_height()

        # Normal button
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Pressed button
        self.image_pressed = pygame.transform.scale(
            image_pressed, (int(width * scale), int(height * scale)))
        self.rect_pressed = self.image_pressed.get_rect()
        self.rect_pressed.topleft = (x, y)

        self.clicked = False
        self.action = False

    def draw(self, surface):
        # Get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        if self.clicked == False:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image_pressed, (self.rect.x, self.rect.y))

        return self.action


class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed

        if self.direction == 1:
            pygame.draw.rect(screen, self.color,
                             (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:
            pygame.draw.rect(screen, self.color,
                             (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= (SCREEN_HEIGHT // 2 + 100):
            fade_complete = True

        return fade_complete


class World():
    def __init__(self):
        self.obstacle_list = []
        self.decoration_list = []
        self.completion_list = []
        self.death_list = []

    def process_data(self, data):
        # Iterate through each row in level csv data file
        for y, row in enumerate(data):
            # Iterate through each cell of the row
            # tile = cell
            for x, tile in enumerate(row):
                # This refers to the value inside the cell/tile and NOT the index/location of the cell!
                if tile >= 0:
                    # Boundry blocks:
                    if tile == 11 or tile == 121 or tile == 123:
                        tile_data = self.tile_processor(tile, x, y)
                        self.obstacle_list.append(tile_data)

                    # Grass blocks & Dirt Blocks & Other regular collision blocks
                    for reg_col_tile in variables.reg_collision_tile_list:
                        if tile == reg_col_tile:
                            tile_data = self.tile_processor(reg_col_tile, x, y)
                            self.obstacle_list.append(tile_data)

                    # Completion blocks (flag)
                    for comp_tile in variables.completion_tile_list:
                        if tile == comp_tile:
                            tile_data = self.tile_processor(tile, x, y)
                            self.completion_list.append(tile_data)

                    # Death blocks
                    if tile == 37:
                        tile_data = self.tile_processor(tile, x, y)
                        self.death_list.append(tile_data)

                    # Decoration blocks
                    for dec_tile in variables.dec_tile_list:
                        if tile == dec_tile:
                            tile_data = self.tile_processor(tile, x, y)
                            self.decoration_list.append(tile_data)

                    # Invisible blocks
                    if tile == 156:
                        tile_data = self.tile_processor(tile, x, y)
                        self.obstacle_list.append(tile_data)

                    # Teleport colission block
                    if tile == 130:
                        tile_data = self.tile_processor(tile, x, y)
                        self.decoration_list.append(tile_data)

                    # Player spawn location
                    if tile == 777:
                        player = Entity(x * TILE_SIZE, y * TILE_SIZE, 1.5, 3)

        return player

    def draw(self):
        for obs_tile in self.obstacle_list:
            obs_tile[1][0] += screen_scroll
            screen.blit(obs_tile[0], obs_tile[1])
        for dec_tile in self.decoration_list:
            dec_tile[1][0] += screen_scroll
            screen.blit(dec_tile[0], dec_tile[1])
        for completion_tile in self.completion_list:
            completion_tile[1][0] += screen_scroll
            screen.blit(completion_tile[0], completion_tile[1])
        for death_tile in self.death_list:
            death_tile[1][0] += screen_scroll
            screen.blit(death_tile[0], death_tile[1])

    def tile_processor(self, tile, x, y):
        img = tile_img_list[tile]
        img_rect = img.get_rect()
        img_rect.x = x * TILE_SIZE
        img_rect.y = y * TILE_SIZE
        tile_data = (img, img_rect, tile)
        return tile_data


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):

        # This init alows you to inherit properties of the sprite class
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.vel_y = 0

        self.flip = False
        self.animation_list = []
        self.frame_index = 0

        # 0 = idle
        # 1 = running
        # 2 = jumping
        self.action = 0

        # Names of the image files
        animation_types = ['Pink_Monster_Idle_4',
                           'Pink_Monster_Run_6', 'Pink_Monster_Jump_6']
        animation_frames = [4, 6, 8]

        self.update_time = pygame.time.get_ticks()

        ####
        ####
        ####

        '''A for loop to load all images and animations properly'''
        for i in range(len(animation_types)):

            # The name of the image file
            animation_type = animation_types[i]

            animation_frames = int(animation_type[-1])
            temp_list = []

            # Load Image
            self.image_sheet = pygame.image.load(
                f'assets/character/{animation_type}.png').convert_alpha()

            for j in range(animation_frames):
                img = self.image_sheet.subsurface(
                    variables.animation_pos_list[i][j])
                img = pygame.transform.scale(
                    img, (img.get_height()*scale, img.get_width()*scale*2))
                temp_list.append(img)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #####
        #####
        #####

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 200
        JUMP_ANIMATION_COOLDOWN = 80
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since last update
        if self.action == 2:
            if pygame.time.get_ticks() - self.update_time > JUMP_ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            # If animation frames run out, restart
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

        else:
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            # If animation frames run out, restart
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def update_action(self, new_action):

        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action

            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):

        if moving_left or moving_right:
            screen.blit(
                # Source
                pygame.transform.flip(self.image, self.flip, False),
                # Destination
                (self.image_rect.x, self.image_rect.y+3))

        else:
            screen.blit(
                # Source
                pygame.transform.flip(self.image, self.flip, False),
                # Destination
                (self.image_rect.x, self.image_rect.y))

    def move(self, moving_left, moving_right):

        # Reset movement variable
        # x and y are the location
        dx = 0
        dy = 0

        # Screen handling
        screen_scroll = 0

        # Assigning movement
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            # Jump height level 8
            self.vel_y = -10
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collision w/ tiles
        for tile in world.obstacle_list:
            # Check collision in x direction
            if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.width, self.height):
                dx = 0

            # Check for collision in y direction
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y + dy, self.width, self.height):
                # Check if below the ground
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = 0

                # Check if above the ground (falling)
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = 0

        # Check collision w/ level completion flag
        level_complete = False
        for tile in world.completion_list:
            if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.width, self.height):
                level_complete_sound.play()
                level_complete = True

        # Check collision w/ teleport block
        for tile in world.decoration_list:
            if tile[2] == 130:
                if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.width, self.height):
                    if level == 5:
                        dx += 450
                        dy -= 400

        # Check collision w/ death block
        for tile in world.death_list:
            if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.width, self.height):
                death_sound.play()
                player.alive = False

        # Check if player goes off edge of screen WIDTH (left/right)
        if self.image_rect.left + dx < 0 or self.image_rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # Check if player falls off edge of screen HEIGHT (bottom/top)
        if self.image_rect.bottom > SCREEN_HEIGHT or self.image_rect.top < 0:
            death_sound.play()
            player.alive = False

        # Update rect position
        self.image_rect.x += dx
        self.image_rect.y += dy

        # Update scroll based on player position
        if self.image_rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.image_rect.left < SCROLL_THRESH:
            self.image_rect.x -= dx
            screen_scroll = -dx

        return screen_scroll, level_complete


'''World Processing & Player Creation & Menu Handling'''

# Buttons & Menu
start_button = Button((SCREEN_WIDTH // 2) - 75,
                      SCREEN_HEIGHT // 2 - 50, start_btn_UP, start_btn_DOWN, 3)

exit_button = Button((SCREEN_WIDTH // 2) - 75,
                     SCREEN_HEIGHT // 2 + 25, exit_btn_UP, exit_btn_DOWN, 3)

restart_button = Button((SCREEN_WIDTH // 2) - 75,
                        SCREEN_HEIGHT // 2 - 50, restart_btn_UP, restart_btn_DOWN, 3)

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# Load in level data csv and create world
with open(f'assets/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()

# TODO: THERES A BIG PROBLEM WITH THIS?!?!
player = world.process_data(world_data)

# Fades
intro_fade = ScreenFade(1, BG, 16)
death_fade = ScreenFade(2, PINK, 12)
''''''

run = True
while run:

    clock.tick(FPS)

    # Interface handling
    if start_game == False and end_game == False:

        if menu_music_playing == False:
            menu_music_playing = True
            menu_music = pygame.mixer.music.load(
                'assets/audio/music/Komiku_-_02_-_Poupis_Theme.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0, 250)

        # Draw bg
        draw_bg()

        # Title Texts
        screen.blit(variables.main_menu_title,
                    (SCREEN_WIDTH // 2 - 215, SCREEN_HEIGHT // 2 - 200))
        screen.blit(variables.how_2_play_text,
                    (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100))
        screen.blit(variables.how_2_play_text_1,
                    (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 130))
        screen.blit(variables.how_2_play_text_2,
                    (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 160))
        screen.blit(variables.how_2_play_text_3,
                    (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 190))
        screen.blit(variables.how_2_play_text_4,
                    (SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 + 220))
        screen.blit(variables.how_2_play_text_5,
                    (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 250))

        # Draw buttons
        if start_button.draw(screen):
            start_game = True

        if exit_button.draw(screen):
            run = False

    elif start_game == True and end_game == False:
        # Play music
        if levels_1to5_music_playing == False:
            levels_1to5_music_playing = True
            levels_1to5_music = pygame.mixer.music.load(
                'assets/audio/music/Fluffing-a-Duck.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0, 250)

        # Update background
        draw_bg()

        # Draw world map
        world.draw()

        # Draw level text indicator:
        level_text = variables.level_text_func(level)
        screen.blit(level_text, (80, 10))

        # mouse_cursor
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # font = pygame.font.SysFont(None, 24)
        # font_img = font.render(f'{mouse_x},{mouse_y}', True, (0, 255, 255))
        # screen.blit(font_img, (mouse_x + 3, mouse_y - 12))

        player.update_animation()
        player.draw()

        intro_fade.fade()

        # Update player actions
        if player.alive:
            if moving_left or moving_right:
                # 1 = run
                player.update_action(1)
            elif player.in_air:
                # 2 = jump
                player.update_action(2)
            else:
                # 0 = idle
                player.update_action(0)

            screen_scroll, level_complete = player.move(
                moving_left, moving_right)

            # Some level handling
            if level == 1:
                GRAVITY = 0.8
                player.speed = 3

            # Level 2
            if level == 2:
                GRAVITY = 0.5

            # Level 3 = Invisible blocks level
            if level == 3:
                GRAVITY = 0.8

            # Level 4 = High speed level
            if level == 4:
                player.speed = 50

            # Level 5 = Teleport level
            if level == 5:
                player.speed = 3

            # Level 5 = Teleport level
            if level == 6:
                player.speed = 1

            if level == 7:
                GRAVITY = 0.9

            if level == 8:
                GRAVITY = 0.4

            if level == 9:
                GRAVITY = 0.13
                player.speed = 20

            if level == 10:
                GRAVITY = 0.3
                player.speed = 3

            # Check if player completed level
            if level_complete:
                level += 1
                level_complete_sound.play()
                world_data = reset_level()

                if level <= MAX_LEVELS:
                    # Load in level data csv and create world
                    with open(f'assets/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    restart_button.action = False
                    world = World()
                    player = world.process_data(world_data)

                else:
                    end_game = True

        else:
            screen_scroll = 0
            if death_fade.fade():
                screen.blit(variables.u_died_text,
                            (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 280))
                screen.blit(variables.game_over_text,
                            (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 200))
                if restart_button.draw(screen):
                    world_data = reset_level()
                    # Load in level data csv and create world
                    with open(f'assets/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    restart_button.action = False
                    world = World()
                    player = world.process_data(world_data)

    elif end_game == True:
        screen_scroll = 0
        screen.blit(variables.game_over_text,
                    (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 200))
        screen.blit(variables.you_win_text,
                    (SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 - 100))
        if exit_button.draw(screen):
            run = False
            pygame.quit()

    for event in pygame.event.get():

        # Key pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                jump_sound.play()
                player.jump = True
            if event.key == pygame.K_SPACE and not player.alive:
                restart_button.action = True

        # Key released
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

        # Quit game
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    pygame.display.update()
