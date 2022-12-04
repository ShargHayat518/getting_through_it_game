import pygame
pygame.init()

# Fonts
# Load Font
comicsans_font_load = pygame.font.SysFont('Comic Sans MS', 60)
comicsans_font_load_medium = pygame.font.SysFont('Comic Sans MS', 48)
comicsans_font_load_small = pygame.font.SysFont('Comic Sans MS', 30)

# Asssign font & text
main_menu_title = comicsans_font_load_medium.render(
    'getting_through_it', True, (0, 0, 0))
u_died_text = comicsans_font_load.render('u died :(', True, (0, 0, 0))
game_over_text = comicsans_font_load.render('Game Over!', True, (0, 0, 0))

how_2_play_text = comicsans_font_load_small.render(
    'how 2 play:', True, (0, 0, 0))
how_2_play_text_1 = comicsans_font_load_small.render(
    'touch the red flag to win', True, (0, 0, 0))
how_2_play_text_2 = comicsans_font_load_small.render(
    'every level is different', True, (0, 0, 0))
how_2_play_text_3 = comicsans_font_load_small.render(
    'some levels are tricky', True, (0, 0, 0))
how_2_play_text_4 = comicsans_font_load_small.render(
    'good luck!', True, (0, 0, 0))

# Animation Lists
Pink_Monster_Idle_4 = [
    # 0
    (5, 3, 19, 28),
    # 1
    (37, 3, 19, 28),
    # 2
    (69, 3, 19, 28),
    # 3
    (101, 3, 19, 28)]

Pink_Monster_Run_6 = [
    # 2
    (71, 5, 18, 26),
    # 3
    (103, 3, 18, 27),
    # 4
    (135, 4, 18, 26),
    # 5
    (167, 5, 18, 26),
    # 0
    (7, 4, 18, 27),
    # 1
    (39, 4, 18, 27),
]

Pink_Monster_Jump_6 = [
    (4, 0, 21, 31),
    (100, 0, 21, 31),
    (132, 0, 21, 31),
    (132, 0, 21, 31),
    (164, 0, 21, 31),
    (228, 0, 21, 31),
]


animation_pos_list = []
animation_pos_list.append(Pink_Monster_Idle_4)
animation_pos_list.append(Pink_Monster_Run_6)
animation_pos_list.append(Pink_Monster_Jump_6)


# Tile Map lists
# Decorative Tiles
dec_tile_list = [1, 2, 26, 28, 56, 57, 65, 66, 70, 71, 93,
                 99, 116, 124, 125, 126, 127, 128, 129, 136, 137]

# Menu button lists
btn_UP = (1, 1, 48, 16)
btn_DOWN = (1, 21, 48, 15)

# Completion tile:
completion_tile_list = [111, 131]
