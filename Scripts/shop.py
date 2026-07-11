#shop.py
import pygame
import settings


class SHOP:
    def __init__(self):
        self.done = False
        self.selected_index = 0

        self.font_title = pygame.font.Font(None, 60)
        self.font_item = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_hint = pygame.font.Font(None, 22)

        self.card_height = 74
        self.card_gap = 14
        self.start_y = 190
        self.padding = 36

        self.previews = {skin["id"]: self._load_preview(skin) for skin in settings.SNAKE_SKINS}

    def _load_preview(self, skin):
        folder = skin["folder"]
        path = f'Graphics/Snake/{folder}/head.png' if folder else 'Graphics/Old/head_right.png'
        try:
            img = pygame.image.load(settings.get_resource_path(path)).convert_alpha()
        except Exception as e:
            print(f"[Shop] Couldn't load preview for {skin['name']}: {e}")
            img = pygame.Surface((48, 48), pygame.SRCALPHA)
        return pygame.transform.smoothscale(img, (48, 48))

    def is_done(self):
        return self.done

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.done = True
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.selected_index = (self.selected_index - 1) % len(settings.SNAKE_SKINS)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.selected_index = (self.selected_index + 1) % len(settings.SNAKE_SKINS)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._interact()

    def _interact(self):
        skin = settings.SNAKE_SKINS[self.selected_index]
        owned = skin["id"] in settings.purchased_skins

        if owned:
            settings.EQUIPPED_SNAKE_SKIN = skin["folder"]
            print(f"[Shop] Equipped {skin['name']}!")
        elif settings.player_coins >= skin["cost"]:
            settings.player_coins -= skin["cost"]
            settings.purchased_skins.add(skin["id"])
            settings.EQUIPPED_SNAKE_SKIN = skin["folder"]
            print(f"[Shop] Purchased and equipped {skin['name']}!")
        else:
            print("[Shop] Not enough coins!")

        settings.save_game_data()

    def update(self):
        pass

    def draw(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 220))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("SNAKE SHOP", True, (255, 215, 0))
        title_outline = self.font_title.render("SNAKE SHOP", True, (20, 20, 30))
        tx = settings.screen_cords // 2 - title.get_width() // 2
        ty = 86
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
            surface.blit(title_outline, (tx + dx, ty + dy))
        surface.blit(title, (tx, ty))

        self._draw_coin_balance(surface)

        for i, skin in enumerate(settings.SNAKE_SKINS):
            self._draw_skin_card(surface, i, skin)

        hint = self.font_hint.render("W/S TO SELECT     ENTER TO BUY / EQUIP     ESC TO EXIT", True, (200, 200, 210))
        hx = settings.screen_cords // 2 - hint.get_width() // 2
        surface.blit(hint, (hx, settings.screen_cords - 46))

    def _draw_coin_balance(self, surface):
        coin_text = self.font_item.render(str(settings.player_coins), True, (255, 255, 255))
        coin_radius = 12
        coin_cx = settings.screen_cords - self.padding - coin_text.get_width() - 30
        coin_cy = 46
        pygame.draw.circle(surface, (255, 215, 0), (coin_cx, coin_cy), coin_radius)
        pygame.draw.circle(surface, (150, 110, 0), (coin_cx, coin_cy), coin_radius, width=2)
        surface.blit(coin_text, (coin_cx + coin_radius + 12, coin_cy - coin_text.get_height() // 2))

    def _draw_skin_card(self, surface, index, skin):
        y = self.start_y + index * (self.card_height + self.card_gap)
        card_rect = pygame.Rect(self.padding, y, settings.screen_cords - self.padding * 2, self.card_height)

        is_selected = (index == self.selected_index)
        owned = skin["id"] in settings.purchased_skins
        equipped = owned and settings.EQUIPPED_SNAKE_SKIN == skin["folder"]

        bg_color = (42, 46, 70) if is_selected else (24, 26, 40)
        border_color = (255, 215, 0) if is_selected else (70, 74, 95)
        pygame.draw.rect(surface, bg_color, card_rect, border_radius=14)
        pygame.draw.rect(surface, border_color, card_rect, width=3 if is_selected else 1, border_radius=14)

        preview = self.previews[skin["id"]]
        preview_bg = pygame.Rect(0, 0, 58, 58)
        preview_bg.midleft = (card_rect.x + 16, card_rect.centery)
        pygame.draw.rect(surface, (12, 12, 22), preview_bg, border_radius=10)
        preview_rect = preview.get_rect(center=preview_bg.center)
        surface.blit(preview, preview_rect)

        name_text = skin["name"]
        if equipped:
            name_text += "  (EQUIPPED)"
        elif owned:
            name_text += "  (OWNED)"
        name_color = (255, 230, 120) if is_selected else (230, 230, 235)
        name_surf = self.font_item.render(name_text, True, name_color)
        surface.blit(name_surf, (preview_bg.right + 20, card_rect.y + 14))

        if equipped:
            status_text, status_color = "ACTIVE", (120, 220, 140)
        elif owned:
            status_text, status_color = "PRESS ENTER TO EQUIP", (200, 200, 210)
        else:
            affordable = settings.player_coins >= skin["cost"]
            status_text = f"{skin['cost']} COINS"
            status_color = (120, 220, 140) if affordable else (230, 100, 100)
        status_surf = self.font_small.render(status_text, True, status_color)
        surface.blit(status_surf, (preview_bg.right + 20, card_rect.y + 44))

        if is_selected:
            arrow = self.font_item.render(">", True, (255, 215, 0))
            surface.blit(arrow, (card_rect.x - 26, card_rect.centery - arrow.get_height() // 2))