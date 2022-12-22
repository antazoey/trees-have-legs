from typing import Iterable

from pygame.sprite import Group

from pharcobial.sprites.base import MobileSprite
from pharcobial.types import Position


class Adversary(MobileSprite):
    pass


class BushMonster(Adversary):
    def __init__(self, position: Position, monster_id: int, groups: Iterable[Group]):
        self.character = "bush-monster"
        super().__init__(position, self.character, groups, Position(0, 26))
        self.monster_id = monster_id
        self.speed = 1

    def get_sprite_id(self) -> str:
        return f"adversary-{self.character}-{self.monster_id}"

    def update(self, *args, **kwargs):
        """
        The monster is always moving towards the player.
        """

        player = self.sprites.player
        new_position = Position(self.rect.x, self.rect.y)

        # Handle x
        if player.rect.x > self.rect.x:
            new_position.x = round(self.rect.x + min(self.speed, player.rect.x - self.rect.x))
        elif player.rect.x < self.rect.x:
            new_position.x = round(self.rect.x - min(self.speed, self.rect.x - player.rect.x))

        # Handle y
        if player.rect.y > self.rect.y:
            new_position.y = round(self.rect.y + min(self.speed, player.rect.y - self.rect.y))
        elif player.rect.y < self.rect.y:
            new_position.y = round(self.rect.y - min(self.speed, self.rect.y - player.rect.y))

        self.move(new_position)
