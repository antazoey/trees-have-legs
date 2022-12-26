from typing import Iterable

from pygame.math import Vector2
from pygame.sprite import Group

from pharcobial.constants import Graphics
from pharcobial.logging import game_logger
from pharcobial.sprites.base import NPC
from pharcobial.types import Positional, SpriteID
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
        self.vision = self.rect.inflate((4 * self.rect.height, 2 * self.rect.width))
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

        player_was_near = self.player_is_near
        if player_was_near:
            # Player is hanging around a tree.
            self.player_is_near = self.vision.colliderect(self.sprites.player.rect)
            if self.player_is_near and self.is_alive:
                self.move_towards_player()

            elif not self.player_is_near and self.is_alive:
                self.sleep()

        else:
            self.player_is_near = self.vision.colliderect(self.sprites.player.rect)
            if self.player_is_near:
                # Player approaches a tree.
                game_logger.debug(f"Player approaches bush {self.bush_index}.")

                # TODO: Have based on difficulty.
                if chance((1, 2)):
                    self.come_alive()

    def sleep(self):
        self.is_alive = False
        game_logger.debug(f"Tree {self.bush_index} going back to sleep.")
        self.set_image(Graphics.BUSH)

    def come_alive(self):
        self.is_alive = True
        game_logger.debug(f"{Graphics.BUSH.capitalize()} {self.bush_index} has come to life!")
        self.set_image(f"{Graphics.BUSH}-monster")
        self.move_towards_player()

    def move_towards_player(self):
        collided_x, collided_y = self.move_towards(self.sprites.player)

        # Deal damage
        player = self.sprites.player
        if (collided_x and collided_x.sprite_id == player.sprite_id) or (
            collided_y and collided_y.sprite_id == player.sprite_id
        ):
            self.deal_damage(player)
