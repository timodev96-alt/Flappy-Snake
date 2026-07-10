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
from death import DEATH
from menu import SETTINGS_MENU, PAUSE_MENU, RESUME, RETURN_TO_TITLE, OPEN_SETTINGS
from shop import SHOP

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

def run_settings_menu(background_snapshot):
    menu = SETTINGS_MENU()
    while not menu.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                menu.update()
            if event.type == pygame.KEYDOWN:
                menu.handle_event(event)

        screen.blit(background_snapshot, (0, 0))
        menu.draw(screen)
        pygame.display.update()
        clock.tick(60)

def run_shop_menu(background_snapshot):
    shop = SHOP()
    while not shop.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                shop.update()
            if event.type == pygame.KEYDOWN:
                shop.handle_event(event)
        screen.blit(background_snapshot,(0,0))
        shop.draw(screen)
        pygame.display.update()
        clock.tick(60)

def run_intro(high_score):
    intro = INTRO(high_score)
    while not intro.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                intro.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and intro.is_waiting():
                    run_settings_menu(screen.copy())
                elif event.key == pygame.K_s and intro.is_waiting():
                    run_shop_menu(screen.copy()) 
                else:
                    intro.handle_event(event)

        work_surface = intro.begin_frame()
        draw_scrolling_bg(work_surface)
        intro.draw()
        intro.present(screen)

        pygame.display.update()
        clock.tick(60)
    return intro

def run_pause_menu(main_game):
    pause_menu = PAUSE_MENU()
    snapshot = screen.copy()
    pygame.mixer.music.pause()

    while not pause_menu.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                pause_menu.update()
            if event.type == pygame.KEYDOWN:
                pause_menu.handle_event(event)
                if pause_menu.result == OPEN_SETTINGS:
                    run_settings_menu(snapshot)
                    pause_menu.result = None

        screen.blit(snapshot, (0, 0))
        pause_menu.draw(screen)
        pygame.display.update()
        clock.tick(60)

    if pause_menu.result == RESUME:
        pygame.mixer.music.unpause()

    return pause_menu.result

def run_game(intro):
    main_game = MAIN()

    body, direction, last_moved_direction = intro.final_snake_state()
    main_game.snake.body = body
    main_game.snake.direction = direction
    main_game.snake.last_moved_direction = last_moved_direction

    occupied = {(int(b.x), int(b.y)) for b in main_game.snake.body}
    while (round(main_game.fruit.pos.x), round(main_game.fruit.pos.y)) in occupied:
        main_game.fruit.randomize()

    while not main_game.is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'Final Score {main_game.score}')
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = run_pause_menu(main_game)
                    if result == RETURN_TO_TITLE:
                        pygame.mixer.music.fadeout(400)
                        return "return_to_title", main_game
                    # RESUME: just keep playing
                else:
                    main_game.inputs(event)

        draw_scrolling_bg(screen)
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

    return "died", main_game


def run_death(main_game):
    death = DEATH(main_game.snake, main_game.pipes, main_game.fruit, main_game.score)
    while not death.is_done():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                death.update()
            if event.type == pygame.KEYDOWN:
                death.handle_event(event)

        work_surface = death.begin_frame()
        draw_scrolling_bg(work_surface)
        death.draw()
        death.present(screen)

        pygame.display.update()
        clock.tick(60)

high_score = 0

while True:
    intro = run_intro(high_score)
    outcome, main_game = run_game(intro)

    if outcome == "died":
        high_score = max(high_score, main_game.score)
        run_death(main_game)