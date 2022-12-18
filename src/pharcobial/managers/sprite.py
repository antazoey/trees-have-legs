import random
from functools import cached_property
from typing import List

from pygame.sprite import Group  # type: ignore

from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.adversary import Adversary, BushMonster
from pharcobial.sprites.base import BaseSprite
from pharcobial.sprites.player import Player


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
        self.sprite_group = Group()
        for sprite in sprites:
            self.sprite_group.add(sprite)

    @cached_property
    def player(self) -> Player:
        character = Player()

        # Put in middle of screen
        character.x = self.display.width // 2
        character.y = self.display.height // 2

        return character

    def __getitem__(self, key: str) -> BaseSprite:
        return self.sprite_map[key]
    
    def __iter__(self):
        yield from self.sprite_group.sprites()

    def create_adversary(self, type_key: str, **kwargs) -> Adversary:
        if type_key == "bush-monster":
            monster = BushMonster(**kwargs)
            monster.x = random.randrange(20, self.display.width - BLOCK_SIZE - 10, 10)
            monster.y = random.randrange(20, self.display.height - BLOCK_SIZE - 10, 10)
            return monster

        else:
            raise TypeError(f"Unsupported adversary type '{type_key}'.")

    def handle_event(self, event):
        for sprite in [s for s in self if s.uses_events]:
            sprite.handle_event(event)

    def update(self):
        self.sprite_group.update()

    def draw(self):
        for sprite in self.sprite_map.values():
            draw_info = sprite.get_draw_info()
            self.display.draw_sprite(draw_info)


sprite_manager = SpriteManager()
