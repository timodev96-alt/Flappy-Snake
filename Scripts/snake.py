import pygame
from pygame.math import Vector2 as V2
import settings
import sprites

class SNAKE:
    def __init__(self):
        self.body = [V2(5,10), V2(4,10), V2(3,10)]
        self.direction = V2(1,0)
        self.last_moved_direction = V2(1,0)
        self.new_block = False
        
        sprites.snake_graphics(self)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * settings.cell_size)
            y_pos = int(block.y * settings.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, settings.cell_size, settings.cell_size)
            
            if index == 0:
                sprites.screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                sprites.screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                p_x = 1 if previous_block.x > 0 else (-1 if previous_block.x < 0 else 0)
                p_y = 1 if previous_block.y > 0 else (-1 if previous_block.y < 0 else 0)
                n_x = 1 if next_block.x > 0 else (-1 if next_block.x < 0 else 0)
                n_y = 1 if next_block.y > 0 else (-1 if next_block.y < 0 else 0)

                if p_x == n_x:
                    sprites.screen.blit(self.body_vertical, block_rect)
                elif p_y == n_y:
                    sprites.screen.blit(self.body_horizontal, block_rect)
                else:
                    if (p_x == -1 and n_y == -1) or (p_y == -1 and n_x == -1):
                        sprites.screen.blit(self.body_tl, block_rect)
                    elif (p_x == -1 and n_y == 1) or (p_y == 1 and n_x == -1):
                        sprites.screen.blit(self.body_bl, block_rect)
                    elif (p_x == 1 and n_y == -1) or (p_y == -1 and n_x == 1):
                        sprites.screen.blit(self.body_tr, block_rect)
                    elif (p_x == 1 and n_y == 1) or (p_y == 1 and n_x == 1):
                        sprites.screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        h_x = 1 if head_relation.x > 0 else (-1 if head_relation.x < 0 else 0)
        h_y = 1 if head_relation.y > 0 else (-1 if head_relation.y < 0 else 0)
        
        if h_x == 1 and h_y == 0: self.head = self.head_left
        elif h_x == -1 and h_y == 0: self.head = self.head_right
        elif h_x == 0 and h_y == 1: self.head = self.head_up
        elif h_x == 0 and h_y == -1: self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        t_x = 1 if tail_relation.x > 0 else (-1 if tail_relation.x < 0 else 0)
        t_y = 1 if tail_relation.y > 0 else (-1 if tail_relation.y < 0 else 0)
        
        if t_x == 1 and t_y == 0: self.tail = self.tail_left
        elif t_x == -1 and t_y == 0: self.tail = self.tail_right
        elif t_x == 0 and t_y == 1: self.tail = self.tail_up
        elif t_x == 0 and t_y == -1: self.tail = self.tail_down

    def move_snake(self):
        self.last_moved_direction = self.direction
        if self.new_block:
            self.body.append(V2(self.body[-1]))
            self.new_block = False
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = V2(self.body[i-1])
        self.body[0] += self.direction

    def add_block(self):
        self.new_block = True