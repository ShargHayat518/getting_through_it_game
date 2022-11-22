import pygame


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
