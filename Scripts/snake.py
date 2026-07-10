#snake.py
import pygame
from pygame.math import Vector2 as V2
import settings
import sprites

_HEAD_SPRITES = {
    (1, 0): 'head_left',
    (-1, 0): 'head_right',
    (0, 1): 'head_up',
    (0, -1): 'head_down',
}
_TAIL_SPRITES = {
    (1, 0): 'tail_left',
    (-1, 0): 'tail_right',
    (0, 1): 'tail_up',
    (0, -1): 'tail_down',
}
_CORNER_SPRITES = {
    frozenset({(-1, 0), (0, -1)}): 'body_tl',
    frozenset({(-1, 0), (0, 1)}): 'body_bl',
    frozenset({(1, 0), (0, -1)}): 'body_tr',
    frozenset({(1, 0), (0, 1)}): 'body_br',
}


def _sign(value):
    return 1 if value > 0 else (-1 if value < 0 else 0)


class SNAKE:
    def __init__(self):
        self.body = [V2(5, 10), V2(4, 10), V2(3, 10)]
        self.direction = V2(1, 0)
        self.last_moved_direction = V2(1, 0)
        self.new_block = False
        self._scaled_cache = {}

        sprites.snake_graphics(self)

    def draw_snake(self, timer_value=9.0):
        if hasattr(self, 'prev_body') and self.prev_body:
            rounded_body = [V2(round(b.x), round(b.y)) for b in self.prev_body]
            if len(rounded_body) < len(self.body):
                rounded_body = [V2(round(b.x), round(b.y)) for b in self.body]
        else:
            rounded_body = [V2(round(b.x), round(b.y)) for b in self.body]

        self.update_head_graphics(rounded_body)
        self.update_tail_graphics(rounded_body)

        lerp_factor = min(1.0, timer_value / 9.0)

        for index, block in enumerate(self.body):
            if hasattr(self, 'prev_body') and index < len(self.prev_body):
                prev_block = self.prev_body[index]
            else:
                prev_block = block

            smooth_x = prev_block.x + (block.x - prev_block.x) * lerp_factor
            smooth_y = prev_block.y + (block.y - prev_block.y) * lerp_factor

            x_pos = int(smooth_x * settings.cell_size)
            y_pos = int(smooth_y * settings.cell_size)
            block_size = int(settings.cell_size * settings.SNAKE_SIZE_SCALE)
            centering_offset = (block_size - settings.cell_size) // 2
            draw_pos = (x_pos - centering_offset, y_pos - centering_offset)

            if index == 0:
                sprites.screen.blit(self._get_scaled(self.head, block_size), draw_pos)
            elif index == len(self.body) - 1:
                sprites.screen.blit(self._get_scaled(self.tail, block_size), draw_pos)
            else:
                sprite = self._body_segment_sprite(rounded_body, index)
                if sprite is not None:
                    sprites.screen.blit(self._get_scaled(sprite, block_size), draw_pos)

    def _get_scaled(self, sprite, size):
        current_tint = settings.EQUIPPED_SNAKE_COLOR
        key = (id(sprite), size, current_tint)
        cached = self._scaled_cache.get(key)
        if cached is None:
            if size != settings.cell_size:
                scaled_surface = pygame.transform.smoothscale(sprite, (size, size))
            else:
                scaled_surface = sprite.copy()
            
            if current_tint != (255, 255, 255):
                tint_surface = pygame.Surface(scaled_surface.get_size(), pygame.SRCALPHA)
                tint_surface.fill((*current_tint, 255))
                scaled_surface.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
            cached = scaled_surface
            self._scaled_cache[key] = cached
        return cached

    def _body_segment_sprite(self, rounded_body, index):
        previous_block = rounded_body[index + 1] - rounded_body[index]
        next_block = rounded_body[index - 1] - rounded_body[index]

        p = (_sign(previous_block.x), _sign(previous_block.y))
        n = (_sign(next_block.x), _sign(next_block.y))

        if p[0] == n[0]:
            return self.body_vertical
        elif p[1] == n[1]:
            return self.body_horizontal
        else:
            attr = _CORNER_SPRITES.get(frozenset({p, n}))
            return getattr(self, attr) if attr else None

    def update_head_graphics(self, rounded_body=None):
        if rounded_body is None:
            rounded_body = self.body

        relation = rounded_body[1] - rounded_body[0]
        attr = _HEAD_SPRITES.get((_sign(relation.x), _sign(relation.y)))
        if attr:
            self.head = getattr(self, attr)

    def update_tail_graphics(self, rounded_body=None):
        if rounded_body is None:
            rounded_body = self.body

        relation = rounded_body[-2] - rounded_body[-1]
        attr = _TAIL_SPRITES.get((_sign(relation.x), _sign(relation.y)))
        if attr:
            self.tail = getattr(self, attr)

    def move_snake(self):
        self.last_moved_direction = self.direction
        if self.new_block:
            self.body.append(V2(self.body[-1]))
            self.new_block = False
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = V2(self.body[i - 1])
        self.body[0] += self.direction

    def add_block(self):
        self.new_block = True