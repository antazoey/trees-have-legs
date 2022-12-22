from functools import cached_property
from typing import Tuple

from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.base import MobileSprite


class Adversary(MobileSprite):
    pass


class BushMonster(Adversary):
    def __init__(self, position: Tuple[int, int], monster_id: int):
        super().__init__(position, "bush-monster")
        self.monster_id = monster_id
        self.speed = 0.2

    @cached_property
    def movement_length(self) -> int:
        return round(BLOCK_SIZE * self.speed)

    def get_sprite_id(self) -> str:
        return str(self.monster_id)

    def update(self, *args, **kwargs):
        """
        The monster is always moving towards the player.
        """

        player = self.sprites.player

        new_x = self.rect.x
        new_y = self.rect.y

        # Handle x
        if player.rect.x > self.rect.x:
            new_x = self.rect.x + min(self.movement_length, player.rect.x - self.rect.x)
        elif player.rect.x < self.rect.x:
            new_x = self.rect.x - min(self.movement_length, self.rect.x - player.rect.x)

        # Handle y
        if player.rect.y > self.rect.y:
            new_y = self.rect.y + min(self.movement_length, player.rect.y - self.rect.y)
        elif player.rect.y < self.rect.y:
            new_y = self.rect.y - min(self.movement_length, self.rect.y - player.rect.y)

        self.move(new_x, new_y)
