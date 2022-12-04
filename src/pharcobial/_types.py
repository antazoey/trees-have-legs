import random
from collections import namedtuple
from enum import Enum
from typing import TYPE_CHECKING, Tuple

from pygame.sprite import Sprite

from pharcobial.constants import DEFAULT_BLOCK_SIZE

if TYPE_CHECKING:
    from pharcobial.display import GameDisplay


Color = Tuple[int, int, int]
Coordinates = namedtuple("Coordinates", ("x", "y"))


class BaseSprite(Sprite):
    x: int = 0
    y: int = 0
    height: int = DEFAULT_BLOCK_SIZE
    width: int = DEFAULT_BLOCK_SIZE

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(self.x, self.y)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class RandomlyAppearing(BaseSprite):
    def __init__(self, display: "GameDisplay"):
        self.display = display
        self.x = random.randrange(20, display.width - display.block_size - 10, 10)
        self.y = random.randrange(20, display.height - display.block_size - 10, 10)
