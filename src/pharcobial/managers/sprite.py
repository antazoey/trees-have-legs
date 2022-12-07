import random
from functools import cached_property
from typing import List

from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.adversary import Adversary, BushMonster
from pharcobial.sprites.base import BaseSprite
from pharcobial.sprites.player import Player

from .base import BaseManager


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()

        # Register all initial sprites here
        sprites: List[BaseSprite] = [
            self.player,
            *[
                self.create_adversary("bush-monster", monster_id=str(i))
                for i in range(self.options.num_monsters)
            ],
        ]

        self.sprite_map = {s.get_sprite_id(): s for s in sprites}

    @cached_property
    def player(self) -> Player:
        character = Player()

        # Put in middle of screen
        character.x = self.display.width // 2
        character.y = self.display.height // 2

        return character

    def __getitem__(self, key: str) -> BaseSprite:
        return self.sprite_map[key]

    def create_adversary(self, type_key: str, **kwargs) -> Adversary:
        if type_key == "bush-monster":
            monster = BushMonster(**kwargs)
            monster.x = random.randrange(20, self.display.width - BLOCK_SIZE - 10, 10)
            monster.y = random.randrange(20, self.display.height - BLOCK_SIZE - 10, 10)
            return monster

        else:
            raise TypeError(f"Unsupported adversary type '{type_key}'.")

    def handle_event(self, event):
        for sprite in [e for e in self.sprite_map.values() if e.uses_events]:
            sprite.handle_event(event)

    def update(self):
        for sprite in self.sprite_map.values():
            sprite.update()

    def draw(self):
        for sprite in self.sprite_map.values():
            draw_info = sprite.get_draw_info()
            self.display.draw_sprite(draw_info)


sprite_manager = SpriteManager()
