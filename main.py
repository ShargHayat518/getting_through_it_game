# Libraries
import pygame
import csv

# Files
import variables

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Getting Through It')


# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.8
SCROLL_THRESH = 200
ROWS = 19
COLS = 25
TILE_SIZE = 32
TILE_TYPES = 179
level = 1

# Defined player action variable
moving_left = False
moving_right = False

# Load background images
level_1_img = pygame.image.load(f'assets/world/backgrounds/04.png')

# Load tile images, store tiles in a list
tile_img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/world/Tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_img_list.append(img)


# Define colors
BG = (0, 0, 0)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    screen.blit(level_1_img, (0, 0))


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # Iterate through each row in level csv data file
        for y, row in enumerate(data):
            # Iterate through each cell of the row
            # tile = cell
            for x, tile in enumerate(row):
                # This refers to the value inside the cell/tile and NOT the index/location of the cell!
                if tile >= 0:
                    # TODO: Change later to determine which blocks are obstacle blocks
                    # Grass blocks
                    if tile == 75:
                        tile_data = self.tile_processor(tile, x, y)
                        self.obstacle_list.append(tile_data)

                        # Dirt blocks
                    if tile == 122:
                        tile_data = self.tile_processor(tile, x, y)
                        self.obstacle_list.append(tile_data)

                        # Player spawn location
                    elif tile == 777:
                        player = Entity(x * TILE_SIZE, y * TILE_SIZE, 1.5, 3)

        return player

    def draw(self):

        for tile in self.obstacle_list:
            tile_temp = (tile[1])
            screen.blit(tile[0], tile[1])

    def tile_processor(self, tile, x, y):
        img = tile_img_list[tile]
        img_rect = img.get_rect()
        img_rect.x = x * TILE_SIZE
        img_rect.y = y * TILE_SIZE
        tile_data = (img, img_rect)
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
                           'Pink_Monster_Run_6_v2', 'Pink_Monster_Jump_6']
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
            # Jump height
            self.vel_y = -10
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collision w/ floor
        for tile in world.obstacle_list:

            # # Check collision in x direction
            if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.width, self.height):
                dx = 0

            # Check for collision in y direction
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y + dy, self.width, self.height):
                # print(f'tile x: {tile[1].x}, tile y: {tile[1].y}, player_x: {self.image_rect.x}, player_y: {self.image_rect.y + dy}, player_center: {self.image_rect.center}, image_rect.midbottom: {self.image_rect.midbottom}')
                # Check if below the ground
                if self.vel_y < 0:
                    pass
                    # TODO: Fix collision when players head hits bottom of a tile
                    self.vel_y = 0
                    dy = 0
                    # dy = tile[1].bottom - self.image_rect.top
                    # print(f'dy: {dy}')
                    # print(f'tile[1].bottom: {tile[1].bottom}')
                    # print(f'self.image_rect.top: {self.image_rect.top}')

                    # Check if above the ground (falling)
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    # dy = tile[1].top - self.image_rect.bottom
                    dy = 0

        # Update rect position
        self.image_rect.x += dx
        self.image_rect.y += dy


# player = Entity(200, 200, 2, 5)

'''World Processing & Player Creation'''
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

# TODO: THERES A BIG PROBLEM WITH THIS!!
player = world.process_data(world_data)
''''''

run = True
while run:

    clock.tick(FPS)

    # Update background
    draw_bg()

    # Draw world map
    world.draw()
    # pygame.draw.line(screen, RED, (288, 428), (SCREEN_WIDTH, 428))
    # pygame.draw.line(screen, RED, (0, 277.5), (SCREEN_WIDTH, 277.5))

    # for x in range(19):
    #     pygame.draw.line(screen, RED, (0, x*32), (SCREEN_WIDTH, x*32))
    # for y in range(25):
    #     pygame.draw.line(screen, RED, (y*32, 0), (y*32, SCREEN_HEIGHT))

    # mouse_cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()

    font = pygame.font.SysFont(None, 24)
    font_img = font.render(f'{mouse_x},{mouse_y}', True, (0, 255, 255))
    screen.blit(font_img, (mouse_x + 3, mouse_y - 12))

    player.update_animation()
    player.draw()
    pygame.draw.line(screen, RED, (0, player.image_rect.top),
                     (SCREEN_WIDTH, player.image_rect.top))

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

        player.move(moving_left, moving_right)

    for event in pygame.event.get():

        # Key pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True

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
