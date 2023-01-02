from typing import Iterable

from pygame.rect import Rect
from pygame.sprite import Group

from pharcobial.constants import Graphics
from pharcobial.logging import game_logger
from pharcobial.sprites.base import NPC, BaseSprite, Character
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
            (-10, -10),
        )
        self.max_speed = 64
        self.vision = self.set_vision()
        self.player_is_near: bool = False
        self.is_alive: bool = False
        self.walk_animation.rate_fn = lambda: 10
        self.walk_animation.prefix = f"{Graphics.TREE}-monster"

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
        if self.is_accessible(player):
            # Attack player.
            self.image = (
                self.graphics.get(f"{Graphics.TREE}-monster-attack", flip_x=self.forward.x < 0)
                or self.image
            )
            self.deal_damage(player)
            return

        scaring = self.hitbox.colliderect(self.sprites.taylor.hitbox.inflate(2, 2))
        if scaring:
            self.sprites.taylor.get_scared(2)

        collision = self.walk_towards(self.sprites.player)

        # Update vision to continuously chase player.
        self.set_vision()

        if collision.x is not None:
            self.inflict(collision.x)
        elif collision.y is not None:
            self.inflict(collision.y)

    def inflict(self, target: BaseSprite):
        if target.sprite_id == self.sprites.player.sprite_id:
            self.set_image("tree-monster-attack")
            self.deal_damage(self.sprites.player)
        elif target.sprite_id == self.sprites.taylor.sprite_id:
            self.sprites.taylor.get_scared(4)

    def set_vision(self) -> Rect:
        self.vision = self.rect.inflate((4 * self.rect.width, 2 * self.rect.height))
        return self.vision

    def deal_damage(self, other: Character):
        self.image = (
            self.graphics.get(f"{Graphics.TREE}-monster-attack", flip_x=self.forward.x < 0)
            or self.image
        )
        return super().deal_damage(other)
