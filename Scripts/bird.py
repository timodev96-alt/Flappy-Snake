#bird.py
import pygame
from pygame.math import Vector2 as V2
import settings
import sprites

class BIRD():
    def __init__(self):
        screen_center_pixels = ((settings.cell_number * settings.cell_size) // 2 ) -80
        self.pos = V2(3 * settings.cell_size, screen_center_pixels)
        self.center_y = screen_center_pixels
        
        self.velocity = 0
        self.gravity = 0.35
        self.jump_strength = -10
        
        self.frame_index = 0
        self.animation_speed = 0.02
        self.angle = 0

        sprites.Bird_graphics(self)
        self.frames = [self.wing_mid , self.wing_up , self.wing_down]

        size_multiplier = 1.4
        orig_w = self.wing_mid.get_width()
        orig_h = self.wing_mid.get_height()
        self.display_width = int(settings.cell_size * size_multiplier)
        self.display_height = int(orig_h * (self.display_width / orig_w))

    def draw_bird(self):
        current_frame = self.frames[int(self.frame_index)]
        
        scaled_frame = pygame.transform.smoothscale(current_frame, (self.display_width, self.display_height))
        rotated_frame = pygame.transform.rotate(scaled_frame, -self.angle)
        bird_rect = rotated_frame.get_rect(center=(int(self.pos.x) + self.display_width // 2, int(self.pos.y) + self.display_height // 2))
        
        sprites.screen.blit(rotated_frame, bird_rect)

    
    def update(self):
        self.velocity += self.gravity
        self.pos.y += self.velocity
        
        if self.pos.y > self.center_y + 65:
            self.jump()
            
        if self.velocity < 0:
            self.angle = -20
            self.animation_speed = 0.30 
        else:
            self.angle += 3.5
            if self.angle > 65: 
                self.angle = 65
            self.animation_speed = 0.05 
            
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
    
    def jump(self):
        self.velocity = self.jump_strength