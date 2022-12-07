from abc import abstractmethod
from typing import Dict

from pygame.sprite import Sprite  # type: ignore

from pharcobial._types import Coordinates, DrawInfo
from pharcobial.constants import BLOCK_SIZE


class BaseSprite(Sprite):
    x: int = 0
    y: int = 0
    height: int = BLOCK_SIZE
    width: int = BLOCK_SIZE
    speed: float = 0
    uses_events: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.previous_coordinates: Coordinates | None = None

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(self.x, self.y)

    @property
    def sprite_map(self) -> Dict:
        """
        Hack to allow sprites to know about each other.
        """
        from pharcobial.managers.sprite import sprite_manager

        return sprite_manager.sprite_map

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """

    @abstractmethod
    def update(self):
        """
        Update properites on the sprite. This gets called after
        event handling.
        """

    def handle_event(self, event):
        """
        Handle events from pygame.
        Method not required for inactive sprites.
        """
        return

    @abstractmethod
    def get_draw_info(self) -> DrawInfo:
        """
        This base method should be called in the subclass overriden method.
        """
