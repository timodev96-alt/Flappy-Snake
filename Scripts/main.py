#main.py
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import pygame
from settings import screen_cords
from sprites import screen, bg_surface, zoomed_width, zoomed_height
from game import MAIN
from intro import INTRO

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 16)

bg_x_pos = 0
bg_scroll_speed = 1


def draw_scrolling_bg(target_surface):
    global bg_x_pos
    bg_x_pos -= bg_scroll_speed
    if bg_x_pos <= -zoomed_width:
        bg_x_pos = 0
    crop_y = (screen_cords - zoomed_height) + 60
    target_surface.blit(bg_surface, (bg_x_pos, crop_y))
    target_surface.blit(bg_surface, (bg_x_pos + zoomed_width, crop_y))
intro = INTRO()

while not intro.is_done():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            intro.update()
        if event.type == pygame.KEYDOWN:
            intro.handle_event(event)

    work_surface = intro.begin_frame()
    draw_scrolling_bg(work_surface)
    intro.draw()
    intro.present(screen)

    pygame.display.update()
    clock.tick(60)

main_game = MAIN()
body, direction, last_moved_direction = intro.final_snake_state()
main_game.snake.body = body
main_game.snake.direction = direction
main_game.snake.last_moved_direction = last_moved_direction

occupied = {(int(b.x), int(b.y)) for b in main_game.snake.body}
while (round(main_game.fruit.pos.x), round(main_game.fruit.pos.y)) in occupied:
    main_game.fruit.randomize()

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

    draw_scrolling_bg(screen)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)