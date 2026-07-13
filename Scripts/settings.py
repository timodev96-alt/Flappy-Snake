#settings.py
import json
import os
import sys
from pathlib import Path

import pygame
from pygame.math import Vector2 as V2

# Grid & Screen Settings
cell_size = 34
cell_number = 25
screen_cords = cell_number * cell_size

# Pipe settings
pipe_speed = 1.9
top_bottom_pipe_space = 4
pipe_to_pipe_space = 500
initial_pipe_delay = 90
PIPE_SPEED_PRESETS = [
    ("EASY", 1.9),
    ("MEDIUM", 2.1),
    ("HARD", 2.6),
]

SNAKE_SIZE_SCALE = 1.2

music_volume = 0.6
MUSIC_VOLUME_STEP = 0.05

COLOR_SCORE_TEXT = (255,255,255)
COLOR_SCORE_BG = (20,20,20,160)
COLOR_SCORE_BORDER = (255,170,0)

player_coins = 0
player_coins = 0

APPLE_TYPES = [
    {
        "id" : "normal",
        "name" : "Apple",
        "chance" : 0.98 , 
        "score_min" : 49 , 
        "score_max" : 74 , 
        "coins" : 5,
        "sprite" : "normal"
    },
    {
        "id" : "golden",
        "name" : "Golden Apple",
        "chance" : 0.02 , 
        "score_min" : 142 ,
        "score_max" : 173 , 
        "coins" : 15,
        "sprite" : "golden"
    },
]

SNAKE_SKINS = [
    {"id": "classic",     "name": "Classic",     "folder": None,          "cost": 0},
    {"id": "coral_snake", "name": "Coral Snake", "folder": "Coral Snake", "cost": 500},
    {"id": "green_mamba", "name": "Green Mamba", "folder": "Green",       "cost": 700},
    {"id": "milk_snake",  "name": "Milk Snake",  "folder": "Milk Snake",  "cost": 900},
]

purchased_skins = {"classic"}
EQUIPPED_SNAKE_SKIN = None
high_score = 0

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_resource_path(*relative_parts):
    candidates = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass))
    candidates.extend([ROOT_DIR, Path(__file__).resolve().parent])

    for base in candidates:
        candidate = base.joinpath(*relative_parts)
        if candidate.exists():
            return str(candidate)
    return str(Path(*relative_parts))


def get_save_path():
    appdata = os.getenv("LOCALAPPDATA")
    if appdata:
        save_dir = Path(appdata) / "FlappySnake"
        save_dir.mkdir(parents=True, exist_ok=True)
        return str(save_dir / "save_data.json")
    return str(ROOT_DIR / "save_data.json")


def save_game_data():
    data = {
        "player_coins": player_coins,
        "pipe_speed": pipe_speed,
        "music_volume": music_volume,
        "purchased_skins": sorted(purchased_skins),
        "equipped_skin": EQUIPPED_SNAKE_SKIN,
        "high_score": high_score,
    }
    save_path = get_save_path()
    try:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    except OSError as exc:
        print(f"[Save] Failed to write save file: {exc}")


def load_game_data():
    save_path = get_save_path()
    if not os.path.exists(save_path):
        return False

    try:
        with open(save_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[Save] Failed to read save file: {exc}")
        return False

    global player_coins, pipe_speed, music_volume, purchased_skins, EQUIPPED_SNAKE_SKIN, high_score
    player_coins = int(data.get("player_coins", player_coins))
    pipe_speed = float(data.get("pipe_speed", pipe_speed))
    music_volume = float(data.get("music_volume", music_volume))
    purchased_skins = set(data.get("purchased_skins", sorted(purchased_skins)))
    EQUIPPED_SNAKE_SKIN = data.get("equipped_skin", EQUIPPED_SNAKE_SKIN)
    high_score = int(data.get("high_score", high_score))
    return True


load_game_data()