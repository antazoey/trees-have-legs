from abc import abstractmethod

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from pharcobial.managers.base import BaseManager


class BaseSprite(Sprite, BaseManager):
    def __init__(self, position: tuple[int, int], gfx_id: str) -> None:
        super().__init__()
        self.image: Surface = self.graphics[gfx_id]
        self.rect: Rect = self.image.get_rect(topleft=position)

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """

    def handle_event(self, event):
        """
        Handle events from pygame.
        Method not required for inactive sprites.
        """
        return


class MobileSprite(BaseSprite):
    speed: float = 0
    direction: Vector2

    def move(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y


__all__ = ["BaseSprite"]
