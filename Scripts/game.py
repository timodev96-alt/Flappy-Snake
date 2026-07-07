import pygame
import sys
import random
from pygame.math import Vector2 as V2
from settings import cell_size, cell_number, pipe_speed
from snake import SNAKE
from fruit import FRUIT
from pipes import PIPES
from bird import BIRD

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.pipes = PIPES()
        self.bird  = BIRD()
        self.snake_timer = 0
        self.score = 0

        self.input_queue = []

    def update(self):
        self.pipes.move_pipes()
        self.pipes.check_and_spawn()
        self.check_lose()
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
        self.bird.draw_bird()

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
            self.fruit.randomize()
            self.snake.add_block()
            fruit_points = random.randint(49, 74)
            print(f'[Debug] Eat apple. added: {fruit_points}')
            self.score += fruit_points

    def check_lose(self):
        head = self.snake.body[0]
        if not -1 <= head.x < cell_number+1 or not -1 <= head.y < cell_number+1:
            print(f'[Debug] Snake out of bounds')
            self.game_over()

        for block in self.snake.body[1:]:
            if round(head.x) == round(block.x) and round(head.y) == round(block.y):
                print(f'[Debug] Snake touched itself')
                self.game_over()

        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size
            if round(head.x) == pipe_grid_x:
                if head.y < pipe['top_end'] or head.y >= pipe['bottom_start']:
                    print("[Debug] Snake head hit a pipe!")
                    self.game_over()

    def check_snake_body_pipe_collision(self):
        push_needed = 0
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] / cell_size
            for block in self.snake.body:
                if abs(block.x - pipe_grid_x) < 0.8:
                    if block.y < pipe['top_end'] or block.y >= pipe['bottom_start']:
                        push_needed = max(push_needed, pipe_speed / cell_size)

        if push_needed:
            for block in self.snake.body:
                block.x -= push_needed

    def game_over(self):
        print(f'Final Score {self.score}')
        pygame.quit()
        sys.exit()

    def check_pipe_passing(self):
        snake_head = self.snake.body[0]
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size
            
            if snake_head.x > pipe_grid_x and not pipe['scored']:
                if pipe['top_end'] <= snake_head.y < pipe['bottom_start']:
                    pipe['scored'] = True
                    pipe_points = random.randint(9, 23)
                    self.score += pipe_points
                    print(f'[Debug] Snake passed through a Pipe.. add score {pipe_points}')