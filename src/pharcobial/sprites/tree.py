from typing import Iterable

from pygame.rect import Rect
from pygame.sprite import Group

from pharcobial.constants import Graphics
from pharcobial.logging import game_logger
from pharcobial.sprites.base import NPC
from pharcobial.types import Positional, SpriteID
from pharcobial.utils import chance


class Tree(NPC):
    def __init__(
        self, sprite_id: SpriteID, position: Positional, groups: Iterable[Group], *args, **kwargs
    ):
        super().__init__(
            sprite_id,
            position,
            Graphics.TREE,
            groups,
            (-30, -26),
        )
        self.max_speed = 64
        self.vision = self.set_vision()
        self.player_is_near: bool = False
        self.is_alive: bool = False
        self.walk_animation.rate_fn = lambda: 10
        self.walk_animation.sprite_id = f"{Graphics.TREE}-monster"

    @property
    def index(self) -> int:
        return int(self.sprite_id.replace(f"{Graphics.TREE}-", ""))

    def update(self, *args, **kwargs):
        """
        When in monster mode, the tree is always moving towards the player.
        Else, it stands still.
        """

        if self.sprites.player.is_dead:
            self.sleep()
            return

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
                game_logger.debug(f"Player approaches tree {self.index}.")

                # TODO: Have based on difficulty.
                if chance((1, 2)):
                    self.come_alive()

    def sleep(self):
        self.is_alive = False
        game_logger.debug(f"Tree {self.index} going back to sleep.")
        self.set_image(Graphics.TREE)

    def come_alive(self):
        self.is_alive = True
        game_logger.debug(f"{Graphics.TREE.capitalize()} {self.index} has come to life!")
        gfx_id = self.walk_animation.get_gfx_id()
        self.set_image(gfx_id)
        self.move_towards_player()

    def move_towards_player(self):
        player = self.sprites.player
        collision = self.walk_towards(self.sprites.player)

        # Update vision to continuously chase player.
        self.set_vision()
        taylor = self.sprites.taylor

        # Deal damage
        if (collision.x and collision.x.sprite_id == player.sprite_id) or (
            collision.y and collision.y.sprite_id == player.sprite_id
        ):
            self.deal_damage(player)

        if (collision.x and collision.x.sprite_id == taylor.sprite_id) or (
            collision.y and collision.y.sprite_id == taylor.sprite_id
        ):
            taylor.get_scared(100)

        elif self.vision.colliderect(taylor.hitbox):
            taylor.get_scared(2)

        else:
            gfx_id = self.walk_animation.get_gfx_id()
            self.set_image(gfx_id)

    def set_vision(self) -> Rect:
        self.vision = self.rect.inflate((4 * self.rect.width, 2 * self.rect.height))
        return self.vision
