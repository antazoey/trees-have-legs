import random
from functools import cached_property
from typing import Dict, List

from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.adversary import Adversary, BushMonster
from pharcobial.sprites.base import BaseSprite
from pharcobial.sprites.player import Player
from pharcobial.sprites.tile import Tile
from pharcobial.types import TileKey


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[str, BaseSprite] = {}
        self.environment_sprites: List[BaseSprite] = []

    def load(self):
        """
        To be called after all managers initialized.
        """
        game_map = list(self.map)
        self.environment_sprites = [
            self.player,
            # Add monsters to camera-followed group
            *[
                self.create_adversary("bush-monster", monster_id=str(i))
                for i in range(self.options.num_monsters)
            ],
            Tile((5 * BLOCK_SIZE, 5 * BLOCK_SIZE), TileKey.ROAD)
            # TODO: Figure out why gets slow when adding more road
            # Add map to camera-followed group
            # *[
            #     Tile((x * BLOCK_SIZE, y * BLOCK_SIZE), tile_key)
            #     for y, row in enumerate(self.map)
            #     for x, tile_key in enumerate(row)
            #     if tile_key != TileKey.GRASS
            # ],
        ]


    @cached_property
    def player(self) -> Player:
        player = Player((self.display.width // 2, self.display.height // 2))
        self._sprite_cache["player"] = player
        return player

    def __getitem__(self, key: str) -> BaseSprite:
        if key in self._sprite_cache:
            return self._sprite_cache[key]

        # Brute force find it and cache it
        for sprite in self.environment_sprites:
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
            return BushMonster((x, y), **kwargs)

        else:
            raise TypeError(f"Unsupported adversary type '{type_key}'.")

    def handle_event(self, event):
        self.player.handle_event(event)


sprite_manager = SpriteManager()
