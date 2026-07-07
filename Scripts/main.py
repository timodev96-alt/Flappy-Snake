import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import pygame
from settings import screen_cords
from sprites import screen, bg_surface, zoomed_width, zoomed_height
from game import MAIN

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 16)

main_game = MAIN()

bg_x_pos = 0
bg_scroll_speed = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f'Final Score {main_game.score}')
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            main_game.inputs(event)

    # Scroller background logic
    bg_x_pos -= bg_scroll_speed
    if bg_x_pos <= -zoomed_width:
        bg_x_pos = 0
    crop_y = (screen_cords - zoomed_height) + 60

    screen.blit(bg_surface, (bg_x_pos, crop_y))
    screen.blit(bg_surface, (bg_x_pos + zoomed_width, crop_y))

    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)