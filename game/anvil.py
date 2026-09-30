import random
import pygame


class Anvil:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.width = 40
        self.height = 32
        self.x = random.randint(20, screen_width - self.width - 20)
        self.y = -self.height
        self.speed = random.uniform(4.5, 7.0)

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def render(self, surface):
        # Calculate speed factor t in [0.0, 1.0] over speed range [4.5, 7.0]
        t = max(0.0, min(1.0, (self.speed - 4.5) / (7.0 - 4.5)))

        # Lerp colors: slow anvils stay grey, fast anvils get strong orange/red accent
        top_color = (
            int(120 + t * (235 - 120)),
            int(120 + t * (90 - 120)),
            int(130 + t * (40 - 130))
        )
        base_color = (
            int(80 + t * (180 - 80)),
            int(80 + t * (50 - 80)),
            int(90 + t * (20 - 90))
        )
        border_color = (
            int(200 + t * (255 - 200)),
            int(200 + t * (150 - 200)),
            int(210 + t * (100 - 210))
        )

        top_rect = pygame.Rect(int(self.x) + 4, int(self.y), self.width - 8, 14)
        pygame.draw.rect(surface, top_color, top_rect, border_radius=2)

        base_rect = pygame.Rect(int(self.x), int(self.y) + 14, self.width, 18)
        pygame.draw.rect(surface, base_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, border_color, base_rect, width=1, border_radius=3)