from pygame.sprite import Group

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager


class CollisionManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.group = Group()

    def validate(self):
        assert self.group is not None
        game_logger.debug("Collision-detection ready.")


collision_manager = CollisionManager()
