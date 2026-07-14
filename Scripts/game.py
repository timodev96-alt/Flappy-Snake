#game.py
import pygame
import random
import math
from pygame.math import Vector2 as V2
import settings
from settings import cell_size, cell_number
from snake import SNAKE
from fruit import FRUIT
from pipes import PIPES
from bird import BIRD


def _in_pipe_gap(pipe, y):
    return pipe['top_end'] <= y < pipe['bottom_start']

def _body_pipe_hitbox():
    return 0.8 * settings.SNAKE_SIZE_SCALE


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.pipes = PIPES()
        self.bird = BIRD()
        self.snake_timer = 0
        self.score = 0
        self.is_over = False
        self._pipe_push_active=False
        self.has_shield = False

        self.input_queue = []

        pygame.font.init()
        self.score_font = pygame.font.SysFont("Arial",32,bold= True)
    def update(self):
        if self.is_over:
            return

        self.pipes.move_pipes()
        self.pipes.check_and_spawn()
        self.check_lose()
        if self.is_over:
            return

        self.bird.update()
        self.check_snake_body_pipe_collision()

        self.snake_timer += 1
        if self.snake_timer >= 9:
            if self.input_queue:
                self.snake.direction = self.input_queue.pop(0)
            self.snake.move_snake()
            self.check_snake_fruit_collision()
            self.check_pipe_passing()
            self.snake_timer = 0

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.pipes.draw_pipes()

    def draw_score_overlay(self, target_surface):
        score_text = f"Score: {self.score}"
        text_surf = self.score_font.render(score_text, True, settings.COLOR_SCORE_TEXT)
        text_rect = text_surf.get_rect()

        padding_x = 20
        padding_y = 10
        width = text_rect.width +(padding_x*2)
        hight = text_rect.height +(padding_y*2)

        x_pos = (target_surface.get_width()-width) // 2
        y_pos = 20

        panel_surf = pygame.Surface((width,hight),pygame.SRCALPHA)
        pygame.draw.rect(panel_surf , settings.COLOR_SCORE_BG,(0,0,width,hight),border_radius=12)
        pygame.draw.rect(panel_surf, settings.COLOR_SCORE_BORDER, (0, 0, width, hight), width=2, border_radius=12)

        panel_surf.blit(text_surf, (padding_x,padding_y))
        target_surface.blit(panel_surf,(x_pos,y_pos))
    def inputs(self, event):
        current_dir = self.input_queue[-1] if self.input_queue else self.snake.last_moved_direction

        if len(self.input_queue) < 2:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if current_dir.y != 1 and (not self.input_queue or self.input_queue[-1] != V2(0, -1)):
                    self.input_queue.append(V2(0, -1))
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if current_dir.y != -1 and (not self.input_queue or self.input_queue[-1] != V2(0, 1)):
                    self.input_queue.append(V2(0, 1))
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if current_dir.x != 1 and (not self.input_queue or self.input_queue[-1] != V2(-1, 0)):
                    self.input_queue.append(V2(-1, 0))
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if current_dir.x != -1 and (not self.input_queue or self.input_queue[-1] != V2(1, 0)):
                    self.input_queue.append(V2(1, 0))

    def check_snake_fruit_collision(self):
        head = self.snake.body[0]
        if round(head.x) == round(self.fruit.pos.x) and round(head.y) == round(self.fruit.pos.y):
            apple_type = self.fruit.apple_type
            self.fruit.randomize()
            self.snake.add_block()
            fruit_points = random.randint(apple_type["score_min"], apple_type["score_max"])
            self.score += fruit_points
            coins_earned = apple_type["coins"]
            settings.player_coins += coins_earned
            settings.save_game_data()
            
            self._apply_apple_effect(apple_type.get("effect"))
            print(f'[Debug] Eat apple.')

    def _apply_apple_effect(self , effect):
        if effect == "shield":
            self.has_shield = True
            print(f"[DEBUG] yay we got shield !")
        elif effect == "wide_gap":
            self.pipes.activate_wide_gap(settings.WIDE_GAP_PIPE_COUNT)
            print(f'[DEBUG] Next {settings.WIDE_GAP_PIPE_COUNT} pipes will be wided')

    def check_lose(self):
        head = self.snake.body[0]
        if not -1 <= head.x < cell_number + 1 or not -1 <= head.y < cell_number + 1:
            print(f'[Debug] Snake out of bounds')
            self.game_over()

        for block in self.snake.body[1:]:
            if round(head.x) == round(block.x) and round(head.y) == round(block.y):
                print(f'[Debug] Snake touched itself')
                self.game_over()

        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size
            if round(head.x) == pipe_grid_x and not _in_pipe_gap(pipe, head.y):
                if self.has_shield:
                    self._break_pipe(pipe)
                else:
                    print("[Debug] Snake head hit a pipe!")
                    self.game_over()

    def _break_pipe(self,pipe):
        self.has_shield = False
        if pipe in self.pipes.pipes_list:
            self.pipes.pipes_list.remove(pipe)
        print(f"[DEBUG] Pipe break")

    def check_snake_body_pipe_collision(self):
        hitbox = _body_pipe_hitbox()
        colliding = False
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] / cell_size
            for block in self.snake.body:
                if abs(block.x - pipe_grid_x) < hitbox and not _in_pipe_gap(pipe, block.y):
                    colliding = True
                    break
            if colliding:
                break
        if colliding:
            push_amount = settings.pipe_speed / cell_size
            for block in self.snake.body:
                block.x -= push_amount
            self._pipe_push_active = True
        elif self._pipe_push_active:
            for blcok in self.snake.body:
                blcok.x = round(blcok.x)
            self._pipe_push_active= False

    def game_over(self):
        if not self.is_over:
            print(f'Final Score {self.score}')
            self.is_over = True

    def check_pipe_passing(self):
        snake_head = self.snake.body[0]
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size

            if snake_head.x > pipe_grid_x and not pipe['scored'] and _in_pipe_gap(pipe, snake_head.y):
                pipe['scored'] = True
                pipe_points = random.randint(9, 23)
                self.score += pipe_points
                print(f'[Debug] Snake passed through a Pipe.. add score {pipe_points}')