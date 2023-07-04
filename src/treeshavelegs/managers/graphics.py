from typing import Dict

import pygame
from pygame.surface import Surface

from treeshavelegs.constants import BLOCK_SIZE, RGB
from treeshavelegs.managers.base import BaseManager
from treeshavelegs.types import GfxID
from treeshavelegs.utils.paths import game_paths


class GraphicsManager(BaseManager):
    gfx_cache: Dict[str, Surface] = {}

    def __getitem__(self, gfx_id: GfxID | None) -> Surface:
        if gfx_id is None:
            return self.get_filled_surface("black")

        gfx = self.get(gfx_id)
        if not gfx:
            raise IndexError(f"Graphics with ID '{gfx_id}' not found.")

        return gfx

    def get(self, gfx_id: GfxID, flip_x: bool = False) -> Surface | None:
        if flip_x:
            # Handle the case where we need to flip the graphic vertically.
            gfx_cache_id = f"{gfx_id}-right"
            if gfx_cache_id in self.gfx_cache:
                return self.gfx_cache[gfx_cache_id]

            gfx = self.get(gfx_id)
            if not gfx:
                return None

            gfx = pygame.transform.flip(gfx, True, False)
            self.gfx_cache[gfx_cache_id] = gfx
            return gfx

        elif gfx_id in self.gfx_cache:
            return self.gfx_cache[gfx_id]

        gfx = self.load(gfx_id)
        self.gfx_cache[gfx_id] = gfx
        return gfx

    def load(self, gfx_id: GfxID) -> Surface:
        path = game_paths.get_graphic(gfx_id)
        gfx = pygame.image.load(path)
        gfx.convert_alpha()  # Allows transparency
        return gfx

    def get_filled_surface(
        self, color: str, width: int = BLOCK_SIZE, height: int = BLOCK_SIZE
    ) -> Surface:
        surface = pygame.Surface((width, height))
        surface.fill(RGB[color])
        return surface


graphics_manager = GraphicsManager()
