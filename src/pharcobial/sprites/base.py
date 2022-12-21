from abc import abstractmethod

from pygame.rect import Rect  # type: ignore
from pygame.sprite import Sprite  # type: ignore

from pharcobial._types import Orientation
from pharcobial.constants import BLOCK_SIZE


class BaseSprite(Sprite):
    speed: float = 0
    uses_events: bool = False
    orientration: Orientation | None
    rect: Rect = Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)

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

    def move(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
