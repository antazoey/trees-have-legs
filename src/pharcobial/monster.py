from typing import TYPE_CHECKING

from pharcobial._types import RandomlyAppearing

if TYPE_CHECKING:
    from pharcobial.display import GameDisplay


class Monster(RandomlyAppearing):
    def __init__(self, display: "GameDisplay", monster_id: int):
        super().__init__(display)
        self.monster_id = monster_id

    def draw(self):
        self.display.draw_image("bush-monster", self.coordinates)
        self.display.beacon.monsters[self.monster_id] = self.coordinates
