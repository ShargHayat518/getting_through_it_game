import pygame
import variables

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Getting Through It')


# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Defined player action variable
moving_left = False
moving_right = False

# Define colors
BG = (0, 0, 0)


def draw_bg():
    screen.fill(BG)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):

        # This init alows you to inherit properties of the sprite class
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.idle_anim_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Testing
        self.idle_animation_sheet_image = pygame.image.load(
            'assets/character/Pink_Monster_Idle_4.png').convert_alpha()

        for i in range(4):
            idle_img_builder = self.idle_animation_sheet_image.subsurface(
                variables.idle_frame_arr[i])
            idle_img_builder = pygame.transform.scale(
                idle_img_builder, (idle_img_builder.get_height()*scale, idle_img_builder.get_width()*scale*2))

            self.idle_anim_list.append(idle_img_builder)

        self.idle_image = self.idle_anim_list[self.frame_index]
        self.idle_image_rect = self.idle_image.get_rect()
        self.idle_image_rect.center = (x, y)

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 200

        # Update image depending on current frame
        self.idle_image = self.idle_anim_list[self.frame_index]

        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If animation frames run out, restart
        if self.frame_index >= len(self.idle_anim_list):
            self.frame_index = 0

    def draw(self):
        # screen.blit(pygame.transform.flip(
        #     self.image, self.flip, False), self.rect)

        screen.blit(pygame.transform.flip(
            self.idle_image, self.flip, False), (self.idle_image_rect.midbottom))

    def move(self, moving_left, moving_right):

        # Reset movement variable
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

        # Update rect position
        self.idle_image_rect.x += dx
        self.idle_image_rect.y += dy


player = Entity(200, 200, 3, 5)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    player.update_animation()
    player.draw()
    player.move(moving_left, moving_right)

    for event in pygame.event.get():

        # Key pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True

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
