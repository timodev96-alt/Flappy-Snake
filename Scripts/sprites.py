#sprites.py
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import settings
from settings import screen_cords, cell_size

pygame.init()

screen = pygame.display.set_mode((screen_cords, screen_cords))

OTHER_DIR = 'Graphics/Other'
SKIN_DIR = 'Graphics/Snake'

DEFAULT_SKIN_FOLDER = settings.get_default_skin()["folder"]
APPLE_DISPLAY_SIZE = 40

def _load(path):
    return pygame.image.load(settings.get_resource_path(path)).convert_alpha()

def _load_apple(filename):
    return pygame.transform.smoothscale(_load(f'{OTHER_DIR}/{filename}'),(APPLE_DISPLAY_SIZE , APPLE_DISPLAY_SIZE))

APPLE_SPRITES = {
    'normal' : _load_apple('Red_apple.png'),
    'golden' : _load_apple('Golden_apple.png'),
    'shield' : _load_apple('Blue_apple.png'),
    'wide_gap' : _load_apple('Green_apple.png'),
}

apple = APPLE_SPRITES['normal']

bg_surface_raw = pygame.image.load(settings.get_resource_path(f'{OTHER_DIR}/bglong.png')).convert()
zoomed_width = int(screen_cords * 2)
zoomed_height = int(screen_cords * 1.5)
bg_surface = pygame.transform.smoothscale(bg_surface_raw, (zoomed_width, zoomed_height))

pipe_raw = _load(f'{OTHER_DIR}/pipe.png')
pipe_w = pipe_raw.get_width()
pipe_h = pipe_raw.get_height()
rim_height = int(pipe_h * 0.25)

BIRD_SPRITE_FILES = {
    'wing_up': 'bird_up',
    'wing_mid': 'bird_mid',
    'wing_down': 'bird_down',
}

def Bird_graphics(self):
    for attr, filename in BIRD_SPRITE_FILES.items():
        setattr(self, attr, _load(f'{OTHER_DIR}/{filename}.png'))

def _load_skin_snake_sprites(skin_folder):
    def frame(part):
        return _load(f'{SKIN_DIR}/{skin_folder}/{part}.png')

    head = frame('head')
    tail = frame('tail')
    body = frame('body')
    corner = frame('corner')

    def rot(img, angle):
        angle = angle % 360
        return pygame.transform.rotate(img, angle) if angle else img

    return {
        'head_right': head,
        'head_up':    rot(head, 90),
        'head_left':  rot(head, 180),
        'head_down':  rot(head, -90),

        'tail_right': rot(tail, 180),
        'tail_up':    rot(tail, -90),
        'tail_left':  tail,
        'tail_down':  rot(tail, 90),

        'body_vertical':   body,
        'body_horizontal': rot(body, 90),

        'body_br': corner,
        'body_bl': rot(corner, -90),
        'body_tl': rot(corner, 180),
        'body_tr': rot(corner, 90),
    }


def snake_graphics(self, skin_folder=None):
    sprite_map = _load_skin_snake_sprites(skin_folder or DEFAULT_SKIN_FOLDER)
    for name, surf in sprite_map.items():
        setattr(self, name, surf)


pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))
pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))