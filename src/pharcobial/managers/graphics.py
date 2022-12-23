from typing import Dict

import pygame
from pygame.surface import Surface

from pharcobial.constants import BLOCK_SIZE, GFX_DIR, RGB
from pharcobial.managers.base import BaseManager


class GraphicsManager(BaseManager):
    gfx_cache: Dict[str, Surface] = {}

    def __getitem__(self, gfx_id: str) -> Surface:
        gfx = self.get(gfx_id)
        if not gfx:
            raise IndexError(f"Graphics with ID '{gfx_id}' not found.")

        return gfx

    def get(self, gfx_id: str, flip_vertically: bool = False) -> Surface | None:
        if flip_vertically:
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

    def load(self, gfx_id: str) -> Surface:
        path = GFX_DIR / f"{gfx_id}.png"
        gfx = pygame.image.load(str(path))
        gfx.convert_alpha()  # Allows transparency
        return gfx

    def get_filled_surface(self, color: str) -> Surface:
        surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        surface.fill(RGB[color])
        return surface


graphics_manager = GraphicsManager()
