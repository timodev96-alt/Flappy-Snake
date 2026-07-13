#fruit.py
import pygame
import random
from pygame.math import Vector2 as V2
import sprites
import settings
from settings import cell_size, cell_number

class FRUIT:
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size) 
        fruit_rect = pygame.Rect(x_pos - 3, y_pos - 3, 40, 40)
        sprite = sprites.APPLE_SPRITES.get(self.apple_type["id"], sprites.apple)
        sprites.screen.blit(sprite , fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = V2(self.x, self.y)
        self.apple_type = self._roll_apple_type()

    def _roll_apple_type(self):
        types = settings.APPLE_TYPES
        weights = [t["chance"] for t in types]
        return random.choices(types, weights = weights ,k=1)[0]