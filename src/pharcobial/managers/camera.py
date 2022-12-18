from pygame.sprite import Group

from pharcobial.managers.base import BaseManager


class CameraManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.group = Group()

        # Put player inside Camera group.
        self.group.add(self.sprites["player"])
