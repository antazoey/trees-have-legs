from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

Color = Tuple[int, int, int]
Coordinates = namedtuple("Coordinates", ("x", "y"))


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


@dataclass
class DrawInfo:
    image_id: str
    coordinates: Coordinates


class GameAction(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"
