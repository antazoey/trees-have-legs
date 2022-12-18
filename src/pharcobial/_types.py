from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from pygame.rect import Rect  # type: ignore

Color = Tuple[int, int, int]


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


@dataclass
class DrawInfo:
    gfx_id: str
    rect: Rect
    orientation: Direction | None = None


class GameAction(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"
