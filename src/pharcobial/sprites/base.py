from abc import abstractmethod
from functools import cached_property
from typing import Dict, Iterable

from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

from pharcobial.managers.base import BaseManager
from pharcobial.types import Positional


class BaseSprite(Sprite, BaseManager):
    def __init__(
        self,
        position: Positional,
        gfx_id: str | None,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional,
    ) -> None:
        super().__init__()
        self.gfx_id = gfx_id
        self.image: Surface = (
            self.graphics[gfx_id] if gfx_id else self.graphics.get_filled_surface("black")
        )
        self.rect: Rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitbox_inflation)
        self.visible = True

        for group in groups:
            group.add(self)

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """

    @cached_property
    def camera_group(self) -> AbstractGroup:
        return [x for x in self.groups() if "camera" in type(x).__name__.lower()][0]

    def dict(self) -> Dict:
        """
        Get a stateful dictionary for reloading.
        """
        return {
            "sprite_id": self.get_sprite_id(),
            "position": {"x": self.rect.x, "y": self.rect.y},
            "gfx_id": self.gfx_id,
        }

    def handle_event(self, event: Event):
        """
        Handle events from pygame.
        Method not required for inactive sprites.
        """
        return

    def set_image(self, gfx_id: str):
        if self.gfx_id != gfx_id:
            self.image = self.graphics[gfx_id]
            self.gfx_id = gfx_id


class MobileSprite(BaseSprite):
    speed: float = 0
    direction: Vector2

    def move(self, x: int, y: int):
        changed = False
        if self.hitbox.x != x:
            self.hitbox.x = x
            self.collision.check_x(self)
            changed = True

        if self.hitbox.y != y:
            self.hitbox.y = y
            self.collision.check_y(self)
            changed = True

        if changed:
            self.rect.center = self.hitbox.center

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0


__all__ = ["BaseSprite"]
