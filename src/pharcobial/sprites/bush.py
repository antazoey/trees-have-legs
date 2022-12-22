from typing import Iterable

from pygame.sprite import Group

from pharcobial.sprites.base import MobileSprite
from pharcobial.types import Position


class Bush(MobileSprite):
    def __init__(self, position: Position, bush_id: str, groups: Iterable[Group]):
        self.character = "bush"
        super().__init__(position, self.character, groups, Position(0, 26))
        self.bush_id = bush_id
        self.speed = 1

    def get_sprite_id(self) -> str:
        return f"adversary-{self.character}-{self.bush_id}"

    def update(self, *args, **kwargs):
        """
        When in monster mode, the bush is always moving towards the player.
        Else, it stands still.
        """

        player = self.sprites.player
        new_position = Position(self.rect.x, self.rect.y)

        return new_position
        # TODO - make conditionally follow and switch image

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
