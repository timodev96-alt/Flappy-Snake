#sprites.py
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from settings import screen_cords, cell_size

pygame.init()

screen = pygame.display.set_mode((screen_cords, screen_cords))

apple = pygame.image.load('Graphics/apple.png').convert_alpha()
bg_surface_raw = pygame.image.load('Graphics/bglong.png').convert()
zoomed_width = int(screen_cords * 2)
zoomed_height = int(screen_cords * 1.5)
bg_surface = pygame.transform.smoothscale(bg_surface_raw, (zoomed_width, zoomed_height))

pipe_raw = pygame.image.load('Graphics/pipe.png').convert_alpha()
pipe_w = pipe_raw.get_width()
pipe_h = pipe_raw.get_height()
rim_height = int(pipe_h * 0.25)


def _load(name):
    return pygame.image.load(f'Graphics/{name}.png').convert_alpha()


SNAKE_SPRITE_NAMES = [
    'head_up', 'head_down', 'head_right', 'head_left',
    'tail_up', 'tail_down', 'tail_right', 'tail_left',
    'body_vertical', 'body_horizontal',
    'body_tr', 'body_tl', 'body_br', 'body_bl',
]

BIRD_SPRITE_FILES = {
    'wing_up': 'bird_up',
    'wing_mid': 'bird_mid',
    'wing_down': 'bird_down',
}


def snake_graphics(self):
    for name in SNAKE_SPRITE_NAMES:
        setattr(self, name, _load(name))


def Bird_graphics(self):
    for attr, filename in BIRD_SPRITE_FILES.items():
        setattr(self, attr, _load(filename))


pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))
pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))