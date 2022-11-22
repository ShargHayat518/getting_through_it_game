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
GRAVITY = 0.75
ROWS = 19
COLS = 25
TILE_SIZE = 32
TILE_TYPES = 179
level = 1

# Defined player action variable
moving_left = False
moving_right = False

# Load images, store tiles in a list
tile_img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load('assets/world/Tiles/{x}}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_img_list.append(img)


# Define colors
BG = (0, 0, 0)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 500), (SCREEN_WIDTH, 500))


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = tile_img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    # TODO: Change later to determine which blocks are obstacle blocks
                    if tile == 0:
                        self.obstacle_list.append(tile_data)
                    elif tile > 0:
                        pass


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
        # screen.blit(pygame.transform.flip(
        #     self.image, self.flip, False), self.rect)

        screen.blit(
            # Source
            pygame.transform.flip(self.image, self.flip, False),
            # Destination
            (self.image_rect.midbottom))

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
            self.vel_y = -13
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check collision w/ floor
        if self.image_rect.bottom + dy > 423:
            dy = 423 - self.image_rect.bottom
            self.in_air = False

        # Update rect position
        self.image_rect.x += dx
        self.image_rect.y += dy


player = Entity(200, 200, 2, 5)

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# Load in level data and create world
with open(f'assets/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    player.update_animation()
    player.draw()

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
