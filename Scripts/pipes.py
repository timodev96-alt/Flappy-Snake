#pipes.py
import pygame
import random
import sprites
import settings
from settings import cell_size, cell_number, top_bottom_pipe_space, pipe_to_pipe_space, initial_pipe_delay
from sprites import pipe_rim_top, pipe_rim_bottom, pipe_body_sprite

class PIPES:
    def __init__(self):
        self.pipes_list = []
        self.pipe_gap = top_bottom_pipe_space
        self.spawn_delay = initial_pipe_delay
        self.delay_timer = 0
        self.first_spawned = False

    def spawn_pipe(self):
        x_pixel_pos = cell_number * cell_size
        top_pipe_end = random.randint(2, cell_number - self.pipe_gap - 2)
        bottom_pipe_start = top_pipe_end + self.pipe_gap
        new_pipe = {
            'x': x_pixel_pos,
            'top_end': top_pipe_end,
            'bottom_start': bottom_pipe_start,
            'spawned_next': False,
            'scored': False
        }
        self.pipes_list.append(new_pipe)

    def move_pipes(self):
        for pipe in self.pipes_list:
            pipe['x'] -= settings.pipe_speed
        self.pipes_list = [pipe for pipe in self.pipes_list if pipe['x'] >= -cell_size]

    def draw_pipes(self):
        if len(self.pipes_list) == 0:
            print(f'[Debug] Pipe List is empty!')
        for pipe in self.pipes_list:
            pipe_x = pipe['x']
            for y in range(0, pipe['top_end']):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)
                if y == pipe['top_end'] - 1:
                    sprites.screen.blit(pipe_rim_top, pipe_rect)
                else:
                    sprites.screen.blit(pipe_body_sprite, pipe_rect)
            for y in range(pipe['bottom_start'], cell_number):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)

                if y == pipe['bottom_start']:
                    sprites.screen.blit(pipe_rim_bottom, pipe_rect)
                else:
                    sprites.screen.blit(pipe_body_sprite, pipe_rect)

    def check_and_spawn(self):
        if not self.first_spawned:
            self.delay_timer += 1
            if self.delay_timer >= self.spawn_delay:
                self.spawn_pipe()
                self.first_spawned = True
            return

        last_pipe = self.pipes_list[-1]
        screen_width_pixels = cell_number * cell_size

        if last_pipe['x'] <= screen_width_pixels - pipe_to_pipe_space and not last_pipe['spawned_next']:
            last_pipe['spawned_next'] = True
            self.spawn_pipe()