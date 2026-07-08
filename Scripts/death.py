#death.py
import random
import pygame
import settings
import sprites

SHAKE, FADE, WAIT, DONE = range(4)

class DEATH:
    def __init__(self, snake, pipes, fruit, score):
        self.state = SHAKE
        self.timer = 0
        self.blink_timer = 0
        self.score = score

        self.snake = snake
        self.pipes = pipes
        self.fruit = fruit

        self.native_screen = sprites.screen
        self.work = pygame.Surface(self.native_screen.get_size()).convert()

        self.shake_mag = 18.0
        self.flash_alpha = 0

        self.font_big = pygame.font.Font(None, 82)
        self.font_small = pygame.font.Font(None, 34)

        pygame.mixer.music.fadeout(600)

    def handle_event(self, event):
        if self.state == WAIT and event.type == pygame.KEYDOWN:
            self.state = DONE

    def update(self):
        self.blink_timer += 1

        if self.state == SHAKE:
            self.timer += 1
            self.shake_mag *= 0.88
            if self.timer > 20:
                self.state = FADE
                self.timer = 0
                self.flash_alpha = 0

        elif self.state == FADE:
            self.timer += 1
            self.flash_alpha = min(235, self.flash_alpha + 12)
            if self.flash_alpha >= 235:
                self.state = WAIT
                self.timer = 0

    def is_done(self):
        return self.state == DONE

    def begin_frame(self):
        sprites.screen = self.work
        return self.work

    def draw(self):
        if self.state in (SHAKE, FADE):
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.pipes.draw_pipes()

        if self.state in (FADE, WAIT):
            overlay = pygame.Surface(self.work.get_size(), pygame.SRCALPHA)
            alpha = self.flash_alpha if self.state == FADE else 235
            overlay.fill((10, 5, 20, alpha))
            self.work.blit(overlay, (0, 0))

        if self.state == WAIT:
            self._draw_game_over_text()

    def present(self, real_screen):
        sprites.screen = real_screen
        if self.state == SHAKE and self.shake_mag > 0.1:
            ox = random.uniform(-self.shake_mag, self.shake_mag)
            oy = random.uniform(-self.shake_mag, self.shake_mag)
            real_screen.blit(self.work, (int(ox), int(oy)))
        else:
            real_screen.blit(self.work, (0, 0))

    def _draw_game_over_text(self):
        title = self.font_big.render("GAME OVER", True, (255, 70, 70))
        title_outline = self.font_big.render("GAME OVER", True, (20, 20, 30))
        tx = settings.screen_cords // 2 - title.get_width() // 2
        ty = 150
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
            self.work.blit(title_outline, (tx + dx, ty + dy))
        self.work.blit(title, (tx, ty))

        score_text = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        sx = settings.screen_cords // 2 - score_text.get_width() // 2
        self.work.blit(score_text, (sx, ty + 90))

        if (self.blink_timer // 24) % 2 == 0:
            prompt = self.font_small.render("PRESS ANY KEY TO PLAY AGAIN", True, (240, 240, 255))
            px = settings.screen_cords // 2 - prompt.get_width() // 2
            py = settings.screen_cords - 140
            self.work.blit(prompt, (px, py))