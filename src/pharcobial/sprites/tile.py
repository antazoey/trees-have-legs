from typing import Iterable, Tuple

from pygame.sprite import Group

from pharcobial.sprites.base import BaseSprite
from pharcobial.types import TileKey


class Tile(BaseSprite):
    def __init__(
        self, position: Tuple[int, int], tile_key: TileKey, groups: Iterable[Group]
    ) -> None:
        self.tile_key = tile_key
        gfx_id = "grass"
        match tile_key:
            case TileKey.ROAD:
                gfx_id = "road"

        super().__init__(position, gfx_id, groups)

    def __repr__(self) -> str:
        return f"<Tile ({self.rect.x}, {self.rect.y}) {self.tile_key.name}>"

    def get_sprite_id(self) -> str:
        return f"tile_({self.rect.x, self.rect.y})"
