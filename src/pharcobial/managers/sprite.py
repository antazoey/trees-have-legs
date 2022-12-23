from functools import cached_property
from typing import Dict, Iterable, List

from pygame.event import Event

from pharcobial.constants import BLOCK_SIZE
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite
from pharcobial.sprites.bush import Bush
from pharcobial.sprites.player import Player
from pharcobial.sprites.tile import Tile
from pharcobial.types import Position, TileKey


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[str, BaseSprite] = {}

    def load(self):
        """
        To be called after all managers initialized.
        """

        _ = self.player
        _ = self.bushes
        _ = self.tiles

    def validate(self):
        assert self.player
        game_logger.debug("Sprites ready.")

    @cached_property
    def player(self) -> Player:
        assert self.map.player_start
        player = Player(self.map.player_start, (self.camera.group, self.collision.group))
        self._sprite_cache["player"] = player
        return player

    @cached_property
    def tiles(self) -> List[Tile]:
        # Find all row boundary tiles.
        # row_boundaries = {}
        # column_boundaries = {}
        # for y, row in enumerate(self.map):
        #     # Find start of row.
        #     for x, tile_key in enumerate(row):
        #         if tile_key == TileKey.VOID:
        #             continue

        #         # Found first non-VOID; seek end and complete row.
        #         for x2, tile_key in enumerate(row[x + 1:]):
        #             if tile_key != TileKey.VOID:
        #                 continue

        #             # Found end of row.
        #             start = min(x - 1, 0)
        #             row_boundaries[y] = (start, x2)

        #         if x not in column_boundaries:
        #             # Is also first non-VOID found for the column.
        #             for y2, row2 in self.map[y+1:]:

        return [
            Tile(Position(x * BLOCK_SIZE, y * BLOCK_SIZE), tile_key, (self.camera.group,))
            for y, row in enumerate(self.map)
            for x, tile_key in enumerate(row)
        ]

    @cached_property
    def bushes(self) -> List[Bush]:
        return [
            Bush(p, str(i), (self.camera.group, self.collision.group))
            for i, p in enumerate(self.map.bushes_start)
        ]

    @property
    def all_sprites(self) -> Iterable[BaseSprite]:
        yield self.player

        for bush in self.bushes:
            yield bush

        for tile in self.tiles:
            yield tile

    def __getitem__(self, key: str) -> BaseSprite:
        if key in self._sprite_cache:
            return self._sprite_cache[key]

        elif key == "player":
            return self.player

        # Brute force find it and cache it
        for sprite in self.all_sprites:
            sprite_id = sprite.get_sprite_id()

            if sprite_id == key:
                # This sprite is likely requested often.
                # Cache for faster look-up next time.
                self._sprite_cache[sprite_id] = sprite
                return sprite

        raise IndexError(f"Sprite with ID '{key}' not found.")

    def handle_event(self, event: Event):
        self.player.handle_event(event)


sprite_manager = SpriteManager()
