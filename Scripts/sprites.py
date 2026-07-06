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

pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))
pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))