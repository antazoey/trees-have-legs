from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite


class CollisionManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.group = Group()

    def validate(self):
        assert self.group is not None
        game_logger.debug("Collision-detection ready.")

    def check(self, hitbox: Rect, direction: Vector2) -> Rect:
        for sprite in self.group.sprites():
            assert isinstance(sprite, BaseSprite)
            if sprite.hitbox.colliderect(hitbox):
                if direction.x > 0:
                    hitbox.right = sprite.hitbox.left
                    break

                elif direction.x < 0:
                    hitbox.left = sprite.hitbox.right
                    break

            elif sprite.hitbox.colliderect(hitbox):
                if direction.y > 0:
                    hitbox.bottom = sprite.hitbox.top
                    break

                elif direction.y < 0:
                    hitbox.top = sprite.hitbox.bottom
                    break

        return hitbox


collision_manager = CollisionManager()
