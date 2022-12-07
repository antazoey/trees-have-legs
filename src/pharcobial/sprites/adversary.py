from abc import abstractmethod

from pharcobial._types import Coordinates, DrawInfo
from pharcobial.constants import BLOCK_SIZE

from .base import BaseSprite


class Adversary(BaseSprite):
    def __init__(self) -> None:
        super().__init__()
        self.previous_coordinates: Coordinates | None = None

    @abstractmethod
    def get_image_id(self) -> str:
        """
        Determines the image used for the adversary.
        """

    def get_draw_info(self) -> DrawInfo:
        return DrawInfo(image_id=self.get_image_id(), coordinates=self.coordinates)


class BushMonster(Adversary):
    def __init__(self, monster_id: int):
        super().__init__()
        self.monster_id = monster_id
        self.speed = 0.2

    def get_image_id(self) -> str:
        return "bush-monster"

    def get_sprite_id(self) -> str:
        return str(self.monster_id)

    def update(self):
        """
        The monster is always moving towards the player.
        """

        movement_length: int = round(BLOCK_SIZE * self.speed)

        player = self.sprite_map["player"]
        if not player:
            return

        new_x = self.x
        new_y = self.y

        # Handle x
        if player.x > self.x:
            new_x = self.x + movement_length
        elif player.x < self.x:
            new_x = self.x - movement_length

        # Handle y
        if player.y > self.y:
            new_y = self.y + movement_length
        elif player.y < self.y:
            new_y = self.y - movement_length

        self.previous_coordinates = self.coordinates
        self.x = new_x
        self.y = new_y
