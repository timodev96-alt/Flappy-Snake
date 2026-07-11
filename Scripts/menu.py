#menu.py
import pygame
import settings

# Pause menu outcomes
RESUME = "resume"
RETURN_TO_TITLE = "return_to_title"
OPEN_SETTINGS = "settings"

SETTINGS_ITEMS = [
    {
        "kind": "choice",
        "label": "PIPE SPEED",
        "attr": "pipe_speed",
        "choices": settings.PIPE_SPEED_PRESETS,
    },
    {
        "kind": "continuous",
        "label": "MUSIC VOLUME",
        "attr": "music_volume",
        "min": 0.0,
        "max": 1.0,
        "step": settings.MUSIC_VOLUME_STEP,
        "fmt": lambda v: f"{round(v * 100)}%",
    },
]

def _closest_choice_index(choices, current_value):
    values = [v for _, v in choices]
    return min(range(len(values)), key=lambda i: abs(values[i] - current_value))


def _display_value(item):
    current = getattr(settings, item["attr"])
    if item["kind"] == "choice":
        idx = _closest_choice_index(item["choices"], current)
        return item["choices"][idx][0]
    return item["fmt"](current)


class SETTINGS_MENU:
    def __init__(self):
        self.selected = 0
        self.done = False
        self.font_title = pygame.font.Font(None, 60)
        self.font_item = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 24)

    def is_done(self):
        return self.done

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.done = True
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.selected = (self.selected - 1) % len(SETTINGS_ITEMS)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.selected = (self.selected + 1) % len(SETTINGS_ITEMS)
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            self._adjust(-1)
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self._adjust(1)

    def _adjust(self, direction):
        item = SETTINGS_ITEMS[self.selected]
        current = getattr(settings, item["attr"])

        if item["kind"] == "choice":
            idx = _closest_choice_index(item["choices"], current)
            idx = (idx + direction) % len(item["choices"])
            new_value = item["choices"][idx][1]
        else:
            new_value = round(max(item["min"], min(item["max"], current + direction * item["step"])), 4)

        setattr(settings, item["attr"], new_value)
        if item["attr"] == "music_volume":
            pygame.mixer.music.set_volume(new_value)
        settings.save_game_data()

    def update(self):
        pass

    def draw(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 215))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("SETTINGS", True, (255, 215, 0))
        tx = settings.screen_cords // 2 - title.get_width() // 2
        surface.blit(title, (tx, 100))

        start_y = 210
        gap = 60
        for i, item in enumerate(SETTINGS_ITEMS):
            line = f"{item['label']}: {_display_value(item)}"
            color = (255, 230, 120) if i == self.selected else (225, 225, 230)
            text = self.font_item.render(line, True, color)
            x = settings.screen_cords // 2 - text.get_width() // 2
            y = start_y + i * gap
            if i == self.selected:
                arrow_l = self.font_item.render("<", True, color)
                arrow_r = self.font_item.render(">", True, color)
                surface.blit(arrow_l, (x - 34, y))
                surface.blit(arrow_r, (x + text.get_width() + 14, y))
            surface.blit(text, (x, y))

        hint = self.font_hint.render("ARROWS TO ADJUST     ESC TO GO BACK", True, (200, 200, 210))
        hx = settings.screen_cords // 2 - hint.get_width() // 2
        surface.blit(hint, (hx, settings.screen_cords - 70))


class PAUSE_MENU:
    OPTIONS = [
        ("SETTINGS", OPEN_SETTINGS),
        ("RETURN TO TITLE", RETURN_TO_TITLE),
    ]

    def __init__(self):
        self.selected = 0
        self.result = None
        self.font_title = pygame.font.Font(None, 64)
        self.font_item = pygame.font.Font(None, 40)
        self.font_hint = pygame.font.Font(None, 24)

    def is_done(self):
        return self.result is not None and self.result != OPEN_SETTINGS

    def update(self):
        pass

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.result = RESUME
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.result = self.OPTIONS[self.selected][1]

    def draw(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 195))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("PAUSED", True, (255, 215, 0))
        tx = settings.screen_cords // 2 - title.get_width() // 2
        surface.blit(title, (tx, 130))

        start_y = 240
        gap = 62
        for i, (label, _action) in enumerate(self.OPTIONS):
            color = (255, 230, 120) if i == self.selected else (225, 225, 230)
            text = self.font_item.render(label, True, color)
            x = settings.screen_cords // 2 - text.get_width() // 2
            y = start_y + i * gap
            surface.blit(text, (x, y))

        hint = self.font_hint.render("ENTER TO SELECT     ESC TO RESUME", True, (200, 200, 210))
        hx = settings.screen_cords // 2 - hint.get_width() // 2
        surface.blit(hint, (hx, settings.screen_cords - 60))