import pygame
import random
from settings import cell_size, cell_number, top_bottom_pipe_space, pipe_speed, pipe_to_pipe_space
from sprites import screen, pipe_rim_top, pipe_rim_bottom, pipe_body_sprite

class PIPES:
    def __init__(self):
        self.pipes_list = []
        self.pipe_gap = top_bottom_pipe_space
        self.pipe_speed = pipe_speed
        self.spawn_pipe()

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
            pipe['x'] -= self.pipe_speed
        self.pipes_list = [pipe for pipe in self.pipes_list if pipe['x'] >= -cell_size]

    def draw_pipes(self):
        if len(self.pipes_list) == 0:
            print(f'[Debug] Pipe List is empty!')
        for pipe in self.pipes_list:
            pipe_x = pipe['x']
            for y in range(0, pipe['top_end']):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)
                if y == pipe['top_end'] - 1:
                    screen.blit(pipe_rim_top, pipe_rect)
                else:
                    screen.blit(pipe_body_sprite, pipe_rect)
            for y in range(pipe['bottom_start'], cell_number):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)
                
                if y == pipe['bottom_start']:
                    screen.blit(pipe_rim_bottom, pipe_rect)
                else:
                    screen.blit(pipe_body_sprite, pipe_rect)

    def check_and_spawn(self):
        if len(self.pipes_list) > 0:
            last_pipe = self.pipes_list[-1]
            screen_width_pixels = cell_number * cell_size
        else:
            self.spawn_pipe()
            return

        if last_pipe['x'] <= screen_width_pixels - pipe_to_pipe_space and not last_pipe['spawned_next']:
            last_pipe['spawned_next'] = True
            self.spawn_pipe()