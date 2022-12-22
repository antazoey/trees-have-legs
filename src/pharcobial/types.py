from enum import Enum
from typing import List, Tuple

Color = Tuple[int, int, int]


class Position(tuple):
    def __new__(cls, *args) -> "Position":
        x_and_y = tuple(args)

        if not len(x_and_y) == 2 or any(not isinstance(v, int) for v in x_and_y):
            raise TypeError(f"{Position.__name__} requires ints x and y to initialize.")

        return super().__new__(cls, x_and_y)

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__()


class GameAction(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"


class TileKey(Enum):
    GRASS = 0
    ROAD = 1
    PLAYER = 2
    BUSH = 3


Map = List[List[TileKey]]
