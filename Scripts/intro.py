import math
import random
import os
import pygame
from pygame.math import Vector2 as V2

import settings
import sprites
from snake import SNAKE
from bird import BIRD

WAIT, APPROACH, FREEZE, SHOCK, EATEN, DONE = range(6)

def _make_sound(freq_start, freq_end, duration, volume=0.35, kind="sine"):
    try:
        import numpy as np
        init = pygame.mixer.get_init()
        if not init: return None
        sample_rate, _, channels = init[0], init[1], init[2]
        n = int(duration * sample_rate)
        t = np.linspace(0, duration, n, endpoint=False)
        freq = np.linspace(freq_start, freq_end, n)
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        if kind == "noise": wave = np.random.uniform(-1, 1, n)
        elif kind == "square": wave = np.sign(np.sin(phase))
        else: wave = np.sin(phase)
        envelope = np.linspace(1, 0, n) ** 1.5
        wave = (wave * envelope * volume * 32767).astype(np.int16)
        if channels == 2: wave = np.column_stack([wave, wave])
        return pygame.sndarray.make_sound(np.ascontiguousarray(wave))
    except Exception: return None

class INTRO:
    def __init__(self, high_score=0):
        self.state = WAIT
        self.timer = 0
        self.blink_timer = 0
        self.high_score = high_score

        self.native_screen = sprites.screen
        self.work = pygame.Surface(self.native_screen.get_size()).convert()
        self.size_multiplier = 1.8 

        self.bg_menu_path = os.path.join("Sound Effects", "Bg_2.mp3")
        self.bg_game_path = os.path.join("Sound Effects", "Bg_1.mp3")
        
        self._play_bg_music(self.bg_menu_path, loops=-1, fade_ms=1000)

        self.bird = BIRD()
        self.bird.pos = V2(settings.cell_size * 5, settings.screen_cords // 2 - 40)
        self.bird.center_y = self.bird.pos.y
        self.bird.velocity = 0
        
        orig_w = self.bird.wing_mid.get_width()
        orig_h = self.bird.wing_mid.get_height()
        self.bird.display_width = int(settings.cell_size * self.size_multiplier)
        self.bird.display_height = int(orig_h * (self.bird.display_width / orig_w))

        bird_center_y = self.bird.pos.y + self.bird.display_height / 2
        self.bird_row = round(bird_center_y / settings.cell_size - 0.5)
        
        self.snake = SNAKE()
        self.snake.body = [V2(-2 - i, self.bird_row) for i in range(4)]
        self.snake.prev_body = [V2(b) for b in self.snake.body]
        self.snake.direction = V2(1, 0)

        self.snake_x_float = -2.0  
        self.creep_speed = 0.04    
        self.dash_speed = 0.22     
        self.is_dashing = False
        self.target_col = (self.bird.pos.x / settings.cell_size) - 1.2

        self.hop_vel = 0.0
        self.hop_offset = 0.0
        self.hop_gravity = 0.42
        self.hop_flap_impulse = -9.0
        self.hop_max_drop = 50

        self.shake_mag = 0.0
        self.zoom = 1.0
        self.pop_scale_x = 1.0
        self.pop_scale_y = 1.0
        self.flash_alpha = 0
        self.grew = False
        self.particles = []

        self.font_big = pygame.font.Font(None, 82)
        self.font_small = pygame.font.Font(None, 34)
        self.font_exclaim = pygame.font.Font(None, 120)

        self.snd_dash = _make_sound(240, 50, 0.45, volume=0.20, kind="noise")
        self.snd_impact = _make_sound(120, 30, 0.25, volume=0.30, kind="square")
        self.snd_gulp = _make_sound(450, 90, 0.35, volume=0.25, kind="sine")
        self._dash_sound_played = False

    def _play_bg_music(self, path, loops=-1, fade_ms=0):
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.15)
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            except Exception as e:
                print(f"Audio stream error loading {path}: {e}")

    def handle_event(self, event):
        if self.state == WAIT and event.type == pygame.KEYDOWN:
            self.state = APPROACH
            self.timer = 0
            
            pygame.mixer.music.fadeout(600)
            
            bird_center_y = self.bird.pos.y + self.bird.display_height / 2
            self.bird_row = round(bird_center_y / settings.cell_size - 0.5)
            
            self.snake_x_float = -2.0
            self.snake.body = [V2(self.snake_x_float - i, self.bird_row) for i in range(4)]
            self.snake.prev_body = [V2(b) for b in self.snake.body]

    def _update_hover_physics(self):
        self.hop_vel += self.hop_gravity
        self.hop_offset += self.hop_vel
        if self.hop_offset > self.hop_max_drop:
            self.hop_offset = self.hop_max_drop
            self.hop_vel = self.hop_flap_impulse

        self.bird.pos.y = self.bird.center_y + self.hop_offset

    def _update_wing_animation(self, fast):
        self.bird.frame_index += 0.25 if fast else 0.08
        if self.bird.frame_index >= len(self.bird.frames):
            self.bird.frame_index = 0

    def _update_hover(self):
        self._update_hover_physics()
        self._update_wing_animation(self.hop_vel < 0)

    def update(self):
        self.blink_timer += 1
        self._decay_camera()

        if self.state == WAIT:
            self._update_hover()

        elif self.state == APPROACH:
            # Keep the wings flapping for feel, but stop the vertical bob once
            # the chase starts - otherwise the bird keeps drifting away from
            # the row the snake is locked onto, and they end up nowhere near
            # each other by the time the snake arrives.
            self._update_wing_animation(fast=True)
            self._update_approach_lerp()

        elif self.state == FREEZE:
            self.timer += 1
            if self.timer > 12: 
                self.state = SHOCK
                self.timer = 0
                self.shake_mag = 24.0
                self.zoom = 1.25
                self._play(self.snd_impact)

        elif self.state == SHOCK:
            self.timer += 1
            self._update_squash_stretch()
            if self.timer > 75:
                self.state = EATEN
                self.timer = 0
                self.flash_alpha = 255  
                self._spawn_feathers()
                self._play(self.snd_gulp)

        elif self.state == EATEN:
            self.timer += 1
            self.flash_alpha = max(0, self.flash_alpha - 4)
            self._update_particles()
            
            if not self.grew and self.timer > 4:
                final_x = round(self.target_col)
                self.snake.body = [V2(final_x - i, self.bird_row) for i in range(4)]
                self.snake.prev_body = [V2(b) for b in self.snake.body]
                
                self.snake.add_block()
                self.grew = True
                
            if self.timer > 90:
                self.state = DONE
                self._play_bg_music(self.bg_game_path, loops=-1, fade_ms=1500)

    def _update_approach_lerp(self):
        distance_left = self.target_col - self.snake_x_float

        if distance_left <= 3.5 and not self.is_dashing:
            self.is_dashing = True
            if not self._dash_sound_played:
                self._play(self.snd_dash)
                self._dash_sound_played = True

        speed = self.dash_speed if self.is_dashing else self.creep_speed
        self.snake_x_float += speed

        if self.snake_x_float >= self.target_col:
            self.snake_x_float = self.target_col
            self.state = FREEZE
            self.timer = 0
            self.shake_mag = 0
            self.zoom = 1.02

        self.snake.body = [V2(self.snake_x_float - i, self.bird_row) for i in range(4)]
        self.snake.prev_body = [V2(self.snake_x_float - i, self.bird_row) for i in range(4)]

        if self.is_dashing:
            self.shake_mag = max(self.shake_mag, 3.5)

    def _update_squash_stretch(self):
        t = self.timer
        if t < 12:
            k = t / 12
            self.pop_scale_x = 1.0 - 0.35 * k
            self.pop_scale_y = 1.0 + 0.55 * k
        elif t < 30:
            k = (t - 12) / 18
            self.pop_scale_x = 0.65 + 0.95 * k
            self.pop_scale_y = 1.55 - 0.95 * k
        else:
            self.pop_scale_x = 1.5
            self.pop_scale_y = 0.6 + 0.3 * min(1.0, (t - 30) / 25)

    def _spawn_feathers(self):
        cx = int(self.bird.pos.x) + self.bird.display_width // 2
        cy = int(self.bird.pos.y) + self.bird.display_height // 2
        colors = [(255, 235, 100), (255, 180, 50), (255, 255, 255), (200, 200, 200)]
        for _ in range(45):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(4.0, 12.0)
            self.particles.append({
                "pos": V2(cx, cy),
                "vel": V2(math.cos(angle) * speed, math.sin(angle) * speed - 4),
                "life": random.randint(25, 50),
                "max_life": 50,
                "color": random.choice(colors),
                "size": random.randint(3, 9),
                "angle": random.uniform(0, 360),
                "rot_speed": random.uniform(-8, 8)
            })

    def _update_particles(self):
        for p in self.particles:
            p["vel"].y += 0.35
            p["pos"] += p["vel"]
            p["angle"] += p["rot_speed"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def _decay_camera(self):
        self.shake_mag *= 0.85
        if self.shake_mag < 0.1:
            self.shake_mag = 0.0
        self.zoom += (1.0 - self.zoom) * 0.12

    def _play(self, sound):
        if sound is not None:
            try: sound.play()
            except Exception: pass

    def is_done(self):
        return self.state == DONE

    def final_snake_state(self):
        body = [V2(round(block.x), round(block.y)) for block in self.snake.body]
        return body, V2(self.snake.direction), V2(self.snake.last_moved_direction)

    def begin_frame(self):
        sprites.screen = self.work
        return self.work

    def draw(self):
        if self.state in (WAIT, APPROACH, FREEZE, SHOCK):
            self._draw_bird()

        if self.state in (APPROACH, FREEZE, SHOCK, EATEN):
            self.snake.draw_snake(9.0)

        if self.state == SHOCK and self.timer > 4:
            self._draw_exclaim()

        if self.state == EATEN:
            self._draw_particles()
            if self.flash_alpha > 0:
                flash_surf = pygame.Surface(self.work.get_size(), pygame.SRCALPHA)
                flash_surf.fill((255, 255, 255, self.flash_alpha))
                self.work.blit(flash_surf, (0, 0))

        if self.state == WAIT:
            self._draw_title_text()

    def present(self, real_screen):
        sprites.screen = real_screen
        if self.zoom > 1.001 or self.shake_mag > 0.01:
            w, h = self.work.get_size()
            zw, zh = int(w * self.zoom), int(h * self.zoom)
            scaled = pygame.transform.smoothscale(self.work, (zw, zh))
            ox = random.uniform(-self.shake_mag, self.shake_mag) - (zw - w) / 2
            oy = random.uniform(-self.shake_mag, self.shake_mag) - (zh - h) / 2
            real_screen.blit(scaled, (int(ox), int(oy)))
        else:
            real_screen.blit(self.work, (0, 0))

    def _draw_bird(self):
        current_frame = self.bird.frames[int(self.bird.frame_index)]
        sx = self.pop_scale_x if self.state == SHOCK else 1.0
        sy = self.pop_scale_y if self.state == SHOCK else 1.0
        w = max(1, int(self.bird.display_width * sx))
        h = max(1, int(self.bird.display_height * sy))
        scaled = pygame.transform.smoothscale(current_frame, (w, h))

        angle = 0
        if self.state in (FREEZE, SHOCK):
            angle = -35 
            scaled = pygame.transform.flip(scaled, True, False)

        rotated = pygame.transform.rotate(scaled, angle)
        center = (
            int(self.bird.pos.x) + self.bird.display_width // 2,
            int(self.bird.pos.y) + self.bird.display_height // 2,
        )
        rect = rotated.get_rect(center=center)
        self.work.blit(rotated, rect)

    def _draw_exclaim(self):
        t = self.timer - 4
        bob = int(10 * math.sin(t * 0.5))
        pop = 1.0 if t > 5 else 0.2 + 0.8 * (t / 5)
        base = self.font_exclaim.render("!", True, (255, 50, 50))
        w, h = base.get_size()
        scaled = pygame.transform.smoothscale(base, (max(1, int(w * pop)), max(1, int(h * pop))))
        outline_base = self.font_exclaim.render("!", True, (255, 255, 255))
        outline = pygame.transform.smoothscale(outline_base, scaled.get_size())
        pos = (
            int(self.bird.pos.x) + self.bird.display_width // 2 - scaled.get_width() // 2,
            int(self.bird.pos.y) - 75 + bob,
        )
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (-4, 0), (4, 0), (0, -4), (0, 4)]:
            self.work.blit(outline, (pos[0] + dx, pos[1] + dy))
        self.work.blit(scaled, pos)

    def _draw_particles(self):
        for p in self.particles:
            rad_x = p["size"]
            rad_y = max(1, p["size"] // 2)
            feather_surf = pygame.Surface((rad_x * 4, rad_x * 4), pygame.SRCALPHA)
            alpha = max(0, int(255 * p["life"] / p["max_life"]))
            color = (*p["color"], alpha)
            pygame.draw.ellipse(feather_surf, color, pygame.Rect(rad_x, rad_x * 1.5, rad_x * 2, rad_y * 2))
            rotated_feather = pygame.transform.rotate(feather_surf, p["angle"])
            f_rect = rotated_feather.get_rect(center=(int(p["pos"].x), int(p["pos"].y)))
            self.work.blit(rotated_feather, f_rect)

    def _draw_title_text(self):
        title = self.font_big.render("FLAPPY SNAKE", True, (255, 215, 0))
        title_outline = self.font_big.render("FLAPPY SNAKE", True, (20, 20, 30))
        tx = settings.screen_cords // 2 - title.get_width() // 2
        ty = 110
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
            self.work.blit(title_outline, (tx + dx, ty + dy))
        self.work.blit(title, (tx, ty))

        high_score_label = f"HIGH SCORE: {self.high_score}"
        high_score_text = self.font_small.render(high_score_label, True, (255, 255, 255))
        high_score_outline = self.font_small.render(high_score_label, True, (20, 20, 30))
        hx = settings.screen_cords // 2 - high_score_text.get_width() // 2
        hy = ty + title.get_height() + 18
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            self.work.blit(high_score_outline, (hx + dx, hy + dy))
        self.work.blit(high_score_text, (hx, hy))

        if (self.blink_timer // 24) % 2 == 0:
            prompt = self.font_small.render("PRESS ANY KEY TO FLY", True, (240, 240, 255))
            px = settings.screen_cords // 2 - prompt.get_width() // 2
            py = settings.screen_cords - 140
            self.work.blit(prompt, (px, py))