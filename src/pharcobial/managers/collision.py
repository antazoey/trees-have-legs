from typing import Callable

from pygame.sprite import Group

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite, MobileSprite


class CollisionManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.group = Group()

    def validate(self):
        assert self.group is not None
        game_logger.debug("Collision-detection ready.")

    def check_x(self, target: MobileSprite):
        def fn(sprite: BaseSprite):
            if not self.collides(target, sprite):
                return True

            if target.direction.x < 0:
                target.hitbox.right += 2 * int(abs(target.direction.x))
                return False

            elif target.direction.x > 0:
                target.hitbox.left -= 2 * int(abs(target.direction.x))
                return False

            return True

        self.for_each(fn)

    def check_y(self, target: MobileSprite):
        def fn(sprite):
            if not self.collides(target, sprite):
                return True

            if target.direction.y < 0:
                target.hitbox.bottom += 2 * int(abs(target.direction.y))
                return False

            elif target.direction.y > 0:
                target.hitbox.top -= 2 * int(abs(target.direction.y))
                return False

            return True

        self.for_each(fn)

    def collides(self, sprite_0: BaseSprite, sprite_1: BaseSprite) -> bool:
        if sprite_0 == sprite_1:
            # Ignore when sprites are the same
            return False

        if sprite_0.hitbox.colliderect(sprite_1.hitbox):
            game_logger.debug(
                f"Collision between '{sprite_0.sprite_id}' " f"and '{sprite_1.sprite_id}' detected."
            )
            return True

        return False

    def for_each(self, fn: Callable):
        for sprite in self.group.sprites():
            assert isinstance(sprite, BaseSprite)
            keep_going = fn(sprite)
            if not keep_going:
                break


collision_manager = CollisionManager()
