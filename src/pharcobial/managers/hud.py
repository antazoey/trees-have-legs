from dataclasses import dataclass
from typing import Dict

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from pharcobial.constants import RGB
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.player import Player
from pharcobial.types import SpriteID


class HUDItem:
    def __init__(self, display_surface: Surface) -> None:
        self.display_surface = display_surface


@dataclass
class InventoryItem:
    name: str
    gfx_id: str
    index: int


class Inventory(HUDItem):
    items: Dict[SpriteID, Dict[int, InventoryItem]] = {}


class HealthBar(HUDItem):
    BAR_HEIGHT = 20
    HEALTH_BAR_WIDTH = 200

    def __init__(self, surface: Surface, start_health: int, max_health: int) -> None:
        super().__init__(surface)
        self.rect = Rect(10, 10, self.HEALTH_BAR_WIDTH, self.BAR_HEIGHT)
        self.current = start_health
        self.max_health = max_health

    def update(self, player: Player):
        self.current = player.hp
        self.max_health = player.max_hp

    def draw(self):
        # Draw background
        pygame.draw.rect(self.display_surface, RGB["black"], self.rect)

        # Convert stat to pixels
        ratio = self.current / self.max_health
        filled_rect = self.rect.copy()
        filled_rect.width = round(self.rect.width * ratio)

        # Draw filled-in health.
        pygame.draw.rect(self.display_surface, RGB["red"], filled_rect)

        # Draw full health-bar border.
        pygame.draw.rect(self.display_surface, RGB["black"], self.rect, 3)


class HUDManager(BaseManager):
    """
    The organizer of the heads-up display
    (a.k.a. the health and inventory items that show on the screen).
    """

    def __init__(self) -> None:
        super().__init__()
        player = self.sprites.player
        self.health_bar = HealthBar(self.display.active.screen, player.hp, player.max_hp)

    def update(self):
        self.health_bar.update(self.sprites.player)

    def draw(self):
        self.health_bar.draw()

    #  self.inventory.draw()


hud_manager = HUDManager()
