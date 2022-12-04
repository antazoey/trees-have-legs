from typing import TYPE_CHECKING

from pharcobial._types import Coordinates
from pharcobial.basesprite import RandomlyAppearing

if TYPE_CHECKING:
    from pharcobial.display import GameDisplay
    from pharcobial.motion import MotionGranter


class Monster(RandomlyAppearing):
    def __init__(self, display: "GameDisplay", motion_granter: "MotionGranter", monster_id: int):
        super().__init__(display, motion_granter)
        self.monster_id = monster_id
        self.previous_coordinates: Coordinates | None = None
        self.move_iterator = 0
        self.move_threshold = 10

    def draw(self):
        self.clear_previous_spot()
        self.display.draw_image("bush-monster", self.coordinates)
        self.display.beacon.monsters[self.monster_id] = self.coordinates

    def move(self):
        player = self.display.beacon.player
        if not player:
            return

        if self.move_iterator <= self.move_threshold:
            self.move_iterator += 1
            return

        self.move_iterator = 0

        new_x = self.x
        new_y = self.y

        # Handle x
        if player.x > self.x:
            new_x = self.x + self.display.block_size
        elif player.x < self.x:
            new_x = self.x - self.display.block_size

        # Handle y
        if player.y > self.y:
            new_y = self.y + self.display.block_size
        elif player.y < self.y:
            new_y = self.y - self.display.block_size

        # TODO: Ensure is not same as other monster
        # other_monsters = {
        #     k: c for k, c in self.display.beacon.monsters.items() if k != self.monster_id
        # }
        # for other in other_monsters:
        #     if o

        self.previous_coordinates = self.coordinates
        self.x = new_x
        self.y = new_y
