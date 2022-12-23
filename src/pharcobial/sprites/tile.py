from typing import Iterable

from pygame.sprite import Group

from pharcobial.sprites.base import BaseSprite
from pharcobial.types import Position, TileKey


class Tile(BaseSprite):
    def __init__(
        self,
        position: Position,
        tile_key: TileKey,
        groups: Iterable[Group],
        is_end_piece: bool = False,  # First layer of X in the map
    ) -> None:
        self.tile_key = tile_key
        gfx_id = None
        match tile_key:
            case TileKey.ROAD:
                gfx_id = "road"
            case TileKey.GRASS:
                gfx_id = "grass"

        hitbox = Position(0, -10)
        self.is_end_piece = is_end_piece
        super().__init__(position, gfx_id, groups, hitbox)

    def __repr__(self) -> str:
        return f"<Tile ({self.rect.x}, {self.rect.y}) {self.tile_key.name}>"

    def get_sprite_id(self) -> str:
        return f"tile_({self.rect.x, self.rect.y})"
