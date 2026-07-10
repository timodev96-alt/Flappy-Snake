import pygame
import sys
import settings
from settings import screen_cords

class SHOP:
    def __init__(self):
        self.done = False
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.selected_index = 0
        
        self.padding = 40
        self.item_height = 80
        self.start_y = 150

    def is_done(self):
        return self.done

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_s):
                self.done = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(settings.SHOP_ITEMS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(settings.SHOP_ITEMS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.interact_with_item()

    def interact_with_item(self):
        item = settings.SHOP_ITEMS[self.selected_index]
        
        if not item["purchased"]:
            if settings.player_coins >= item["cost"]:
                settings.player_coins -= item["cost"]
                item["purchased"] = True
                print(f"[Shop] Purchased {item['name']}!")
            else:
                print("[Shop] Not enough coins!")
        else:
            if item["type"] == "snake_tint":
                settings.EQUIPPED_SNAKE_COLOR = item["value"]
                print(f"[Shop] Equipped Tint Profile: {item['name']}!")

    def update(self):
        pass

    def draw(self, surface):
        overlay = pygame.Surface((screen_cords, screen_cords), pygame.SRCALPHA)
        overlay.fill((15, 22, 38, 220)) 
        surface.blit(overlay, (0, 0))

        title_surf = self.font.render("--- SNAKE COZY SHOP ---", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen_cords // 2, 50))
        surface.blit(title_surf, title_rect)

        wallet_surf = self.font.render(f"Coins: {settings.player_coins}", True, (255, 215, 0))
        wallet_rect = wallet_surf.get_rect(topright=(screen_cords - self.padding, 40))
        surface.blit(wallet_surf, wallet_rect)

        for i, item in enumerate(settings.SHOP_ITEMS):
            current_y = int(self.start_y) + (int(i) * (int(self.item_height) + 15))
            
            card_rect = pygame.Rect(self.padding, current_y, screen_cords - (self.padding * 2), self.item_height)
            
            is_selected = (i == self.selected_index)
            bg_color = (40, 50, 75) if is_selected else (25, 30, 45)
            border_color = (255, 215, 0) if is_selected else (60, 70, 90)
            border_width = 3 if is_selected else 1

            pygame.draw.rect(surface, bg_color, card_rect, border_radius=10)
            pygame.draw.rect(surface, border_color, card_rect, width=border_width, border_radius=10)

            preview_rect = pygame.Rect(card_rect.x + 15, card_rect.y + 15, 50, 50)
            
            preview_color = item["value"] if item["value"] != (255, 255, 255) else (200, 200, 200)
            pygame.draw.rect(surface, preview_color, preview_rect, border_radius=6)

            name_text = item["name"]
            if item["type"] == "snake_tint" and settings.EQUIPPED_SNAKE_COLOR == item["value"]:
                name_text += " (EQUIPPED)"
            elif item["purchased"]:
                name_text += " (OWNED)"

            name_surf = self.small_font.render(name_text, True, (255, 255, 255))
            surface.blit(name_surf, (preview_rect.right + 20, card_rect.y + 15))

            if not item["purchased"]:
                price_text = f"{item['cost']} Coins"
                price_color = (255, 100, 100) if settings.player_coins < item["cost"] else (100, 255, 100)
            else:
                price_text = "Press Enter to Equip" if not (item["type"] == "snake_tint" and settings.EQUIPPED_SNAKE_COLOR == item["value"]) else "Active"
                price_color = (150, 200, 150) if settings.EQUIPPED_SNAKE_COLOR == item["value"] else (200, 200, 200)

            price_surf = self.small_font.render(price_text, True, price_color)
            price_rect = price_surf.get_rect(midright=(card_rect.right - 20, card_rect.centery))
            surface.blit(price_surf, price_rect)

        nav_surf = self.small_font.render("Use W/S or UP/DOWN to Select | Enter to Action | Press 'S' or 'ESC' to Exit", True, (150, 150, 150))
        nav_rect = nav_surf.get_rect(center=(screen_cords // 2, screen_cords - 40))
        surface.blit(nav_surf, nav_rect)