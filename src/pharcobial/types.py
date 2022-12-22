from enum import Enum
from typing import List, Tuple

Color = Tuple[int, int, int]


class GameAction(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"


class TileKey(Enum):
    GRASS = 0
    ROAD = 1


Map = List[List[TileKey]]
