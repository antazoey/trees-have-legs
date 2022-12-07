import random
from abc import abstractmethod
from typing import TYPE_CHECKING

from pygame.sprite import Sprite  # type: ignore

from pharcobial._types import Coordinates
from pharcobial.constants import DEFAULT_BLOCK_SIZE

if TYPE_CHECKING:
    from pharcobial.display import GameDisplay


class Beacon(dict):
    """
    A mappping of sprite IDs to coordinates.
    """


_beacon = Beacon(player=None)


class BaseSprite(Sprite):
    x: int = 0
    y: int = 0
    height: int = DEFAULT_BLOCK_SIZE
    width: int = DEFAULT_BLOCK_SIZE
    speed: float = 0

    def __init__(self, display: "GameDisplay") -> None:
        super().__init__()
        self.display = display
        self.previous_coordinates: Coordinates | None = None

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(self.x, self.y)

    @property
    def beacon_ref(self) -> Beacon:
        return _beacon

    @abstractmethod
    def get_sprite_id(self) -> str:
        """
        Return a unique identifier for this sprite.
        """

    def draw(self):
        _beacon[self.get_sprite_id()] = self.coordinates

    def clear_previous_spot(self):
        if self.previous_coordinates:
            size = self.display.block_size * 2
            self.display.draw_rect("white", self.previous_coordinates, width=size, height=size)


class RandomlyAppearing(BaseSprite):
    def __init__(self, display: "GameDisplay"):
        super().__init__(display)
        self.x = random.randrange(20, display.width - display.block_size - 10, 10)
        self.y = random.randrange(20, display.height - display.block_size - 10, 10)
