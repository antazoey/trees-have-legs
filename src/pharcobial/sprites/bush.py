from typing import Iterable

from pygame.math import Vector2
from pygame.sprite import Group

from pharcobial.logging import game_logger
from pharcobial.sprites.base import BaseSprite, MobileSprite
from pharcobial.types import Position
from pharcobial.utils import chance


class Bush(MobileSprite):
    def __init__(self, position: Position, bush_id: str, groups: Iterable[Group]):
        self.character = "bush"
        super().__init__(position, self.character, groups, (-30, -26))
        self.bush_id = bush_id
        self.speed = 1
        self.vision = self.rect.inflate((2 * self.rect.height, 2 * self.rect.width))
        self.direction = Vector2()
        self.player_is_near: bool = False
        self.is_alive: bool = False

    def get_sprite_id(self) -> str:
        return f"adversary-{self.character}-{self.bush_id}"

    def update(self, *args, **kwargs):
        """
        When in monster mode, the bush is always moving towards the player.
        Else, it stands still.
        """

        player = self.sprites.player
        player_was_near = self.player_is_near
        if player_was_near:
            # Player is hanging around a tree.
            self.player_is_near = self.vision.colliderect(self.sprites.player.rect)
            if self.player_is_near and self.is_alive:
                self.move_towards(player)

            elif not self.player_is_near and self.is_alive:
                # Player has escaped a tree that was chasing.
                game_logger.debug(f"Tree {self.bush_id} going back to sleep.")
                self.image = self.graphics["bush"]

        else:
            self.player_is_near = self.vision.colliderect(self.sprites.player.rect)
            if self.player_is_near:
                # Player approaches a tree.
                game_logger.debug(f"Player approaches bush {self.bush_id}.")

                self.is_alive = chance((1, 4))
                if self.is_alive:
                    # Tree is now going to chase you for a bit.
                    game_logger.debug(f"Bush {self.bush_id} has come to life!")
                    self.image = self.graphics["bush-monster"]
                    self.move_towards(player)

    def move_towards(self, sprite: BaseSprite):
        new_position = Position(self.rect.x, self.rect.y)

        # Handle x
        if sprite.rect.x > self.rect.x:
            new_position.x = round(self.rect.x + min(self.speed, sprite.rect.x - self.rect.x))
            self.direction.x = 1
        elif sprite.rect.x < self.rect.x:
            new_position.x = round(self.rect.x - min(self.speed, self.rect.x - sprite.rect.x))
            self.direction.x = -1

        # Handle y
        if sprite.rect.y > self.rect.y:
            new_position.y = round(self.rect.y + min(self.speed, sprite.rect.y - self.rect.y))
            self.direction.y = 1
        elif sprite.rect.y < self.rect.y:
            new_position.y = round(self.rect.y - min(self.speed, self.rect.y - sprite.rect.y))
            self.direction.y = -1

        self.rect.x = new_position.x
        self.rect.y = new_position.y
