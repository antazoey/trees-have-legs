from pathlib import Path
from typing import Dict

import pygame  # type: ignore
from pygame.surface import Surface  # type: ignore

from pharcobial._types import Direction

from .base import BaseManager


class GraphicsManager(BaseManager):
    base_path = Path(__file__).parent.parent.parent.parent / "gfx"
    image_cache: Dict = {}

    def __getitem__(self, gfx_id: str):
        return self.get(gfx_id)

    def get(self, gfx_id: str, orientation: Direction | None = None) -> Surface:
        if orientation == Direction.RIGHT:
            # Handle the case where we need to flip the image vertically.
            image_cache_id = f"{gfx_id}-{Direction.RIGHT.value}"
            if image_cache_id in self.image_cache:
                return self.image_cache[image_cache_id]

            image = self.get(gfx_id)
            image = pygame.transform.flip(image, True, False)
            self.image_cache[image_cache_id] = image
            return image

        elif gfx_id in self.image_cache:
            return self.image_cache[gfx_id]

        image = self.load(gfx_id)
        self.image_cache[gfx_id] = image
        return image

    def load(self, gfx_id: str):
        path = self.base_path / f"{gfx_id}.png"
        image = pygame.image.load(str(path))
        image.convert_alpha()  # Allows transparency
        return image


graphics_manager = GraphicsManager()
