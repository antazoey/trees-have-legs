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

    def check_x(self, target: MobileSprite) -> BaseSprite | None:
        def fn(sprite: BaseSprite):
            if not self.collides(target, sprite):
                return None

            elif target.direction.x < 0:
                target.hitbox.right += 2 * int(abs(target.direction.x))
                return sprite

            elif target.direction.x > 0:
                target.hitbox.left -= 2 * int(abs(target.direction.x))
                return sprite

            # Not sure it's possible  to get here.
            return None

        return self._check(fn)

    def check_y(self, target: MobileSprite) -> BaseSprite | None:
        def fn(sprite):
            if not self.collides(target, sprite):
                return None

            el if target.direction.y < 0:
                target.hitbox.bottom += 2 * int(abs(target.direction.y))
                return sprite

            elif target.direction.y > 0:
                target.hitbox.top -= 2 * int(abs(target.direction.y))
                return sprite

            # Not sure it's possible  to get here.
            return None

        return self._check(fn)

    def collides(self, sprite_0: BaseSprite, sprite_1: BaseSprite) -> bool:
        if sprite_0 == sprite_1:
            # Ignore when sprites are the same
            return False

        if sprite_0.hitbox.colliderect(sprite_1.hitbox):
            id_0 = sprite_0.sprite_id
            id_1 = sprite_1.sprite_id
            game_logger.debug(f"Collision between '{id_0}' and '{id_1}' detected.")
            return True

        return False

    def _check(self, fn: Callable) -> BaseSprite | None:
        for sprite in self.group.sprites():
            assert isinstance(sprite, BaseSprite)
            collided = fn(sprite)
            if collided is not None:
                return collided

        return None


collision_manager = CollisionManager()
