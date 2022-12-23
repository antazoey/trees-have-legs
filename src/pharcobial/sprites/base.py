from abc import abstractmethod
from typing import Iterable, Tuple, Dict

from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from pharcobial.managers.base import BaseManager
from pharcobial.types import Position


class BaseSprite(Sprite, BaseManager):
    def __init__(
        self,
        position: Position,
        gfx_id: str | None,
        groups: Iterable[Group],
        hitbox_inflation: Position | Tuple[int, int],
    ) -> None:
        super().__init__()
        self.image: Surface = (
            self.graphics[gfx_id] if gfx_id else self.graphics.get_filled_surface("black")
        )
        self.rect: Rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitbox_inflation)

        for group in groups:
            group.add(self)

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """
    
    def dict(self) -> Dict:
        """
        Get a stateful dictionary for reloading.
        """
        return {
            "sprite_id": self.get_sprite_id(),
            "position": {"x": self.rect.x, "y": self.rect.y},
            "gfx_id": self.image.gfx_id,
        }

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
        self.hitbox.x = position.x
        self.collision.check_x(self)
        self.hitbox.y = position.y
        self.collision.check_y(self)
        self.rect.center = self.hitbox.center

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0


__all__ = ["BaseSprite"]
