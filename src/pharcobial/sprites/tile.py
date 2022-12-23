from typing import Iterable

from pygame.sprite import Group

from pharcobial.sprites.base import BaseSprite
from pharcobial.types import Positional, TileKey


class Tile(BaseSprite):
    def __init__(
        self,
        position: Positional,
        tile_key: TileKey,
        groups: Iterable[Group],
    ) -> None:
        self.tile_key = tile_key
        gfx_id = None
        match tile_key:
            case TileKey.ROAD:
                gfx_id = "road"
                hitbox = (0, 0)
            case TileKey.GRASS:
                gfx_id = "grass"
                hitbox = (0, 0)
            case TileKey.VOID:
                gfx_id = None
                hitbox = (-10, 0)

        super().__init__(f"tile_({position[0]}, {position[1]})", position, gfx_id, groups, hitbox)

    def __repr__(self) -> str:
        return f"<Tile ({self.rect.x}, {self.rect.y}) {self.tile_key.name}>"
