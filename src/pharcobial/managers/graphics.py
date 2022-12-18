from pathlib import Path
from typing import Dict

import pygame  # type: ignore
from pygame.surface import Surface  # type: ignore

from pharcobial._types import Direction

from .base import BaseManager


class GraphicsManager(BaseManager):
    base_path = Path(__file__).parent.parent.parent.parent / "gfx"
    gfx_cache: Dict = {}

    def __getitem__(self, gfx_id: str) -> Surface:
        gfx = self.get(gfx_id)
        if not gfx:
            raise IndexError(f"Graphics with ID '{gfx_id}' not found.")

        return gfx

    def get(self, gfx_id: str, orientation: Direction | None = None) -> Surface | None:
        if orientation == Direction.RIGHT:
            # Handle the case where we need to flip the image vertically.
            gfx_cache_id = f"{gfx_id}-{Direction.RIGHT.value}"
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

        try:
            gfx = self.load(gfx_id)
        except Exception:
            return None

        self.gfx_cache[gfx_id] = gfx
        return gfx

    def load(self, gfx_id: str) -> Surface:
        path = self.base_path / f"{gfx_id}.png"
        gfx = pygame.image.load(str(path))
        gfx.convert_alpha()  # Allows transparency
        return gfx


graphics_manager = GraphicsManager()
