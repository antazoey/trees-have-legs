from abc import abstractmethod
from typing import Iterable, Tuple, cast

from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from pharcobial.managers.base import BaseManager
from pharcobial.types import Position


class BaseSprite(Sprite, BaseManager):
    def __init__(
        self, position: Position, gfx_id: str, groups: Iterable[Group], hitbox_inflation: Position
    ) -> None:
        super().__init__()
        self.image: Surface = self.graphics[gfx_id]
        self.rect: Rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitbox_inflation)

        for group in groups:
            group.add(self)

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """

    def handle_event(self, event: Event):
        """
        Handle events from pygame.
        Method not required for inactive sprites.
        """
        return


class MobileSprite(BaseSprite):
    speed: float = 0
    direction: Vector2

    def move(self, position: Position):
        self.hitbox.topleft = cast(Tuple[int, int], position)
        self.rect.center = self.hitbox.center


__all__ = ["BaseSprite"]
