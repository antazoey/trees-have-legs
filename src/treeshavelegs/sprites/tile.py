from typing import Iterable

from pygame.sprite import Group

from treeshavelegs.constants import MAP_VOID
from treeshavelegs.sprites.base import BaseSprite
from treeshavelegs.types import Positional, TileKey


class Tile(BaseSprite):
    def __init__(
        self,
        position: Positional,
        tile_key: TileKey,
        hitbox: Positional | None,
        groups: Iterable[Group],
    ) -> None:
        self.tile_key = tile_key
        gfx_id = self.map.tile_set[tile_key]["gfx"]
        super().__init__(
            f"tile_({position[0]}, {position[1]})",
            gfx_id,
            groups,
            position=position,
            hitbox_inflation=hitbox,
        )

    def __repr__(self) -> str:
        return f"<Tile ({self.rect.x}, {self.rect.y}) {self.tile_key}>"


class Ground(Tile):
    def __init__(self, position: Positional, tile_key: TileKey, collision: bool) -> None:
        groups = (self.world.group, self.collision.group) if collision else (self.world.group,)
        super().__init__(position, tile_key, None, groups)


class Void(Tile):
    def __init__(self, position: Positional) -> None:
        super().__init__(position, MAP_VOID, (0, 0), (self.world.group, self.collision.group))
