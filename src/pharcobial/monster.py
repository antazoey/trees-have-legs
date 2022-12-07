from typing import TYPE_CHECKING

from pharcobial._types import Coordinates
from pharcobial.basesprite import RandomlyAppearing

if TYPE_CHECKING:
    from pharcobial.collision import CollisionDetector
    from pharcobial.display import GameDisplay


class Monster(RandomlyAppearing):
    def __init__(
        self, display: "GameDisplay", collision_detector: "CollisionDetector", monster_id: int
    ):
        super().__init__(display, collision_detector)
        self.monster_id = monster_id
        self.previous_coordinates: Coordinates | None = None
        self.speed = 0.2

    def draw(self):
        # self.clear_previous_spot()
        self.display.draw_image("bush-monster", self.coordinates)
        self.display.beacon.monsters[self.monster_id] = self.coordinates

    def move(self):
        """
        The monster is always moving towards the player.
        """

        movement_length: int = round(self.display.block_size * self.speed)

        player = self.display.beacon.player
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
