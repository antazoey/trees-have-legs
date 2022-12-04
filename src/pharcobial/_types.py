from collections import namedtuple
from enum import Enum
from typing import Tuple

Color = Tuple[int, int, int]
Coordinates = namedtuple("Coordinates", ("x", "y"))


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
