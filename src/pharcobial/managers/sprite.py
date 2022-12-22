import random
from functools import cached_property
from typing import Dict, Iterable, List

from pharcobial.constants import BLOCK_SIZE
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.adversary import Adversary, BushMonster
from pharcobial.sprites.base import BaseSprite
from pharcobial.sprites.player import Player
from pharcobial.sprites.tile import Tile
from pharcobial.types import Position


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[str, BaseSprite] = {}

    def load(self):
        """
        To be called after all managers initialized.
        """

        _ = self.player
        _ = self.adversaries
        _ = self.tiles

    def validate(self):
        assert self.player
        game_logger.debug("Sprites ready.")

    @cached_property
    def player(self) -> Player:
        position = Position(self.display.width // 2, self.display.height // 2)
        player = Player(position, (self.camera.group, self.collision.group))
        self._sprite_cache["player"] = player
        return player

    @cached_property
    def adversaries(self) -> List[Adversary]:
        return [
            self.create_adversary("bush-monster", monster_id=str(i))
            for i in range(self.options.num_monsters)
        ]

    @cached_property
    def tiles(self) -> List[Tile]:
        return [
            Tile(Position(x * BLOCK_SIZE, y * BLOCK_SIZE), tile_key, (self.camera.group,))
            for y, row in enumerate(self.map)
            for x, tile_key in enumerate(row)
        ]

    @property
    def all_sprites(self) -> Iterable[BaseSprite]:
        yield self.player

        for adversary in self.adversaries:
            yield adversary

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

    def create_adversary(self, type_key: str, **kwargs) -> Adversary:
        if type_key == "bush-monster":
            x = random.randrange(20, self.display.width - BLOCK_SIZE - 10, 10)
            y = random.randrange(20, self.display.height - BLOCK_SIZE - 10, 10)
            pos = Position(x, y)
            return BushMonster(
                pos,
                kwargs["monster_id"],
                (self.camera.group, self.collision.group),
            )

        else:
            raise TypeError(f"Unsupported adversary type '{type_key}'.")

    def handle_event(self, event):
        self.player.handle_event(event)


sprite_manager = SpriteManager()
