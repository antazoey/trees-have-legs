from dataclasses import dataclass
from typing import Dict

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from pharcobial.constants import BLOCK_SIZE, RGB
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.player import Player
from pharcobial.sprites.taylor import Taylor
from pharcobial.types import Positional, SpriteID


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


class Bar(HUDItem):
    def __init__(
        self,
        surface: Surface,
        position: Positional,
        height: int,
        width: int,
        color: str,
        start: int,
        max: int,
        horizontal: bool = True,
    ) -> None:
        super().__init__(surface)
        self.height = height
        self.width = width
        self.color = color
        self.rect = Rect(*position, self.width, self.height)  # type: ignore
        self.current = start
        self.max = max
        self.horizontal = horizontal

    def draw(self):
        # Draw background
        pygame.draw.rect(self.display_surface, RGB["onyx"], self.rect)

        # Convert stat to pixels
        ratio = self.current / self.max
        filled_rect = self.rect.copy()
        if self.horizontal:
            filled_rect.width = round(self.rect.width * ratio)
        else:
            height = round(self.rect.height * ratio)
            offset = self.rect.height - height
            filled_rect.y += offset
            filled_rect.height = height

        # Draw filled-in health.
        pygame.draw.rect(self.display_surface, RGB[self.color], filled_rect)

        # Draw full health-bar border.
        pygame.draw.rect(self.display_surface, RGB["black"], self.rect, 3)


class HealthBar(Bar):
    def __init__(self, surface: Surface, start_health: int, max_health: int) -> None:
        super().__init__(surface, (10, 10), 20, 128, "red", start_health, max_health)

    def update(self, player: Player):
        self.current = player.hp
        self.max = player.max_hp


class TaylorCalmBar(Bar):
    def __init__(self, surface: Surface, hysteria: int, max_hysteria: int) -> None:
        super().__init__(
            surface,
            (surface.get_width() - 2 * BLOCK_SIZE, 10),
            128,
            20,
            "blue",
            hysteria,
            max_hysteria,
            horizontal=False,
        )

    def update(self, taylor: Taylor):
        self.current = taylor.hysteria


class HUDManager(BaseManager):
    """
    The organizer of the heads-up display
    (a.k.a. the health and inventory items that show on the screen).
    """

    def __init__(self) -> None:
        super().__init__()
        player = self.sprites.player
        self.health_bar = HealthBar(self.display.active.screen, player.hp, player.max_hp)
        self.taylor_calm_bar = TaylorCalmBar(
            self.display.active.screen, self.sprites.taylor.hysteria, 100
        )

    def update(self):
        self.health_bar.update(self.sprites.player)
        self.taylor_calm_bar.update(self.sprites.taylor)

    def draw(self):
        self.health_bar.draw()
        self.taylor_calm_bar.draw()

    #  self.inventory.draw()


hud_manager = HUDManager()
