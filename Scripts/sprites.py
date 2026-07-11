#sprites.py
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import settings
from settings import screen_cords, cell_size

pygame.init()

screen = pygame.display.set_mode((screen_cords, screen_cords))

LEGACY_DIR = 'Graphics/Old'
SKIN_DIR = 'Graphics/Snake'


def _load(path):
    return pygame.image.load(settings.get_resource_path(path)).convert_alpha()


apple = _load(f'{LEGACY_DIR}/apple.png')
bg_surface_raw = pygame.image.load(settings.get_resource_path(f'{LEGACY_DIR}/bglong.png')).convert()
zoomed_width = int(screen_cords * 2)
zoomed_height = int(screen_cords * 1.5)
bg_surface = pygame.transform.smoothscale(bg_surface_raw, (zoomed_width, zoomed_height))

pipe_raw = _load(f'{LEGACY_DIR}/pipe.png')
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
        setattr(self, attr, _load(f'{LEGACY_DIR}/{filename}.png'))

LEGACY_SNAKE_NAMES = [
    'head_up', 'head_down', 'head_right', 'head_left',
    'tail_up', 'tail_down', 'tail_right', 'tail_left',
    'body_vertical', 'body_horizontal',
    'body_tr', 'body_tl', 'body_br', 'body_bl',
]


def _load_legacy_snake_sprites():
    return {name: _load(f'{LEGACY_DIR}/{name}.png') for name in LEGACY_SNAKE_NAMES}

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
    sprite_map = _load_legacy_snake_sprites() if skin_folder is None else _load_skin_snake_sprites(skin_folder)
    for name, surf in sprite_map.items():
        setattr(self, name, surf)


pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))
pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))