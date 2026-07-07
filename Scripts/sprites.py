import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from settings import screen_cords, cell_size

pygame.init()

# Setup Screen
screen = pygame.display.set_mode((screen_cords, screen_cords))

# Fruits & Background
apple = pygame.image.load('Graphics/apple.png').convert_alpha() 
bg_surface_raw = pygame.image.load('Graphics/bglong.png').convert()
zoomed_width = int(screen_cords * 2)
zoomed_height = int(screen_cords * 1.5)
bg_surface = pygame.transform.smoothscale(bg_surface_raw, (zoomed_width, zoomed_height))

# Pipes Sprites Processing
pipe_raw = pygame.image.load('Graphics/pipe.png').convert_alpha()
pipe_w = pipe_raw.get_width()
pipe_h = pipe_raw.get_height()
rim_height = int(pipe_h * 0.25)

#Snake
def snake_graphics(self):
    self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
    self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
    self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
    self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

def Bird_graphics(self):
    self.wing_up = pygame.image.load('Graphics/bird_up.png').convert_alpha()
    self.wing_mid = pygame.image.load('Graphics/bird_mid.png').convert_alpha()
    self.wing_down = pygame.image.load('Graphics/bird_down.png').convert_alpha()

pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))
pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))