import pygame
import random
from pygame.math import Vector2 as V2
from settings import cell_size, cell_number
from sprites import screen, apple

class FRUIT:
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size) 
        fruit_rect = pygame.Rect(x_pos - 3, y_pos - 3, 40, 40)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = V2(self.x, self.y)