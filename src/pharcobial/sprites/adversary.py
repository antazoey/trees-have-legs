from abc import abstractmethod
from functools import cached_property

from pharcobial._types import DrawInfo
from pharcobial.constants import BLOCK_SIZE

from .base import BaseSprite


class Adversary(BaseSprite):
    @abstractmethod
    def get_gfx_id(self) -> str:
        """
        Determines the image used for the adversary.
        """

    def get_draw_info(self) -> DrawInfo:
        return DrawInfo(gfx_id=self.get_gfx_id(), rect=self.coordinates)


class BushMonster(Adversary):
    def __init__(self, monster_id: int):
        super().__init__()
        self.monster_id = monster_id
        self.speed = 0.2

    @cached_property
    def movement_length(self) -> int:
        return round(BLOCK_SIZE * self.speed)

    def get_gfx_id(self) -> str:
        return "bush-monster"

    def get_sprite_id(self) -> str:
        return str(self.monster_id)

    def update(self, *args, **kwargs):
        """
        The monster is always moving towards the player.
        """

        player = self.sprite_map["player"]

        new_x = self.x
        new_y = self.y

        # Handle x
        if player.x > self.x:
            new_x = self.x + min(self.movement_length, player.x - self.x)
        elif player.x < self.x:
            new_x = self.x - min(self.movement_length, self.x - player.x)

        # Handle y
        if player.y > self.y:
            new_y = self.y + min(self.movement_length, player.y - self.y)
        elif player.y < self.y:
            new_y = self.y - min(self.movement_length, self.y - player.y)

        self.x = new_x
        self.y = new_y
