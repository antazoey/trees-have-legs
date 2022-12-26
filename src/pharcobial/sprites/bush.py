from typing import Iterable

from pygame.math import Vector2
from pygame.sprite import Group

from pharcobial.constants import Graphics
from pharcobial.logging import game_logger
from pharcobial.sprites.base import NPC, BaseSprite
from pharcobial.types import Position, Positional, SpriteID
from pharcobial.utils import chance


class Bush(NPC):
    def __init__(
        self, sprite_id: SpriteID, position: Positional, groups: Iterable[Group], *args, **kwargs
    ):
        super().__init__(
            sprite_id,
            position,
            Graphics.BUSH,
            groups,
            (-30, -26),
        )
        self.speed = 1
        self.vision = self.rect.inflate((2 * self.rect.height, 2 * self.rect.width))
        self.direction = Vector2()
        self.player_is_near: bool = False
        self.is_alive: bool = False

    @property
    def bush_index(self) -> int:
        return int(self.sprite_id.replace(f"{Graphics.BUSH}-", ""))

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
                game_logger.debug(f"Tree {self.bush_index} going back to sleep.")
                self.set_image(Graphics.BUSH)

        else:
            self.player_is_near = self.vision.colliderect(self.sprites.player.rect)
            if self.player_is_near:
                # Player approaches a tree.
                game_logger.debug(f"Player approaches bush {self.bush_index}.")

                self.is_alive = chance((1, 2))
                if self.is_alive:
                    # Tree is now going to chase you for a bit.
                    game_logger.debug(
                        f"{Graphics.BUSH.capitalize()} {self.bush_index} has come to life!"
                    )
                    self.set_image(f"{Graphics.BUSH}-monster")
                    self.move_towards(player)

    def move_towards(self, sprite: BaseSprite):
        new_position = Position(self.hitbox.x, self.hitbox.y)

        # Handle x
        if sprite.hitbox.x > self.hitbox.x:
            new_position.x = round(self.hitbox.x + min(self.speed, sprite.hitbox.x - self.hitbox.x))
            self.direction.x = 1
        elif sprite.hitbox.x < self.hitbox.x:
            new_position.x = round(self.hitbox.x - min(self.speed, self.hitbox.x - sprite.hitbox.x))
            self.direction.x = -1

        # Handle y
        if sprite.hitbox.y > self.hitbox.y:
            new_position.y = round(self.hitbox.y + min(self.speed, sprite.hitbox.y - self.hitbox.y))
            self.direction.y = 1
        elif sprite.hitbox.y < self.hitbox.y:
            new_position.y = round(self.hitbox.y - min(self.speed, self.hitbox.y - sprite.hitbox.y))
            self.direction.y = -1

        self.move(new_position.x, new_position.y)
