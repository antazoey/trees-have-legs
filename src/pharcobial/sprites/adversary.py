from functools import cached_property
from typing import Iterable, Tuple

from pygame.sprite import Group

from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.base import MobileSprite


class Adversary(MobileSprite):
    pass


class BushMonster(Adversary):
    def __init__(self, position: Tuple[int, int], monster_id: int, groups: Iterable[Group]):
        self.character = "bush-monster"
        super().__init__(position, self.character, groups)
        self.monster_id = monster_id
        self.speed = 1

    def get_sprite_id(self) -> str:
        return f"adversary-{self.character}-{self.monster_id}"

    def update(self, *args, **kwargs):
        """
        The monster is always moving towards the player.
        """

        player = self.sprites.player

        new_x = self.rect.x
        new_y = self.rect.y

        # Handle x
        if player.rect.x > self.rect.x:
            new_x = self.rect.x + min(self.speed, player.rect.x - self.rect.x)
        elif player.rect.x < self.rect.x:
            new_x = self.rect.x - min(self.speed, self.rect.x - player.rect.x)

        # Handle y
        if player.rect.y > self.rect.y:
            new_y = self.rect.y + min(self.speed, player.rect.y - self.rect.y)
        elif player.rect.y < self.rect.y:
            new_y = self.rect.y - min(self.speed, self.rect.y - player.rect.y)

        self.move(new_x, new_y)
