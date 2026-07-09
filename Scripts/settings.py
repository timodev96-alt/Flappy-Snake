#settings.py
import pygame
from pygame.math import Vector2 as V2

# Grid & Screen Settings
cell_size = 34
cell_number = 25
screen_cords = cell_number * cell_size

# Pipe settings
pipe_speed = 2.6
top_bottom_pipe_space = 4
pipe_to_pipe_space = 500
initial_pipe_delay = 90

PIPE_SPEED_PRESETS = [
    ("EASY", 1.8),
    ("MEDIUM", 2.1),
    ("HARD", 2.6),
]
SNAKE_SIZE_SCALE = 1.2

# Audio
music_volume = 0.6
MUSIC_VOLUME_STEP = 0.05

# Color Settings
BG_COLOR = (10, 23, 250)
SNAKE_COLOR = (183, 111, 122)
FRUIT_COLOR = (194, 54, 22)
PIPE_COLOR = (34, 139, 30)