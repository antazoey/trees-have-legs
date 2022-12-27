from typing import Tuple

from pygame.sprite import Group

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite, MobileSprite
from pharcobial.types import Positional


class CollisionManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.group = Group()

    def validate(self):
        assert self.group is not None
        game_logger.debug("Collision-detection ready.")

    def collides(self, sprite_0: BaseSprite, sprite_1: BaseSprite) -> bool:
        if sprite_0.sprite_id == sprite_1.sprite_id:
            # Ignore when sprites are the same
            return False

        elif sprite_0.hitbox.colliderect(sprite_1.hitbox):
            id_0 = sprite_0.sprite_id
            id_1 = sprite_1.sprite_id
            game_logger.debug(f"Collision between '{id_0}' and '{id_1}' detected.")
            return True

        return False

    def check(self, target: MobileSprite, position: Positional) -> Tuple[BaseSprite | None, BaseSprite | None]:
        collides_x = None
        collides_y = None

        for sprite in self.group.sprites():
            assert isinstance(sprite, BaseSprite)  # For Mypy

            if collides_x and collides_y:
                # Both found.
                return collides_x, collides_y
            
            target.hitbox.x = position.x
            if not self.collides(target, sprite):
                # Non-collision.
                continue

            elif not collides_x and target.direction.x < 0 or target.direction.x > 0:
                # X collision found.
                collides_x = sprite

            elif not collides_y and target.direction.y < 0 or target.direction.y > 0:
                # Y collision found.
                collides_y = sprite

        return collides_x, collides_y


collision_manager = CollisionManager()
