from enum import Enum
from typing import List, Tuple, Union

Color = Tuple[int, int, int]


class Position(tuple):
    def __new__(cls, *args) -> "Position":
        x_and_y = tuple(args)
        return super().__new__(cls, x_and_y)

    def __init__(self, x: Union[int, "Positional"], y: int | None = None) -> None:
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y
        elif isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]

        super().__init__()


Positional = Tuple[int, int] | Position


class GameAction(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"


class TileKey(Enum):
    GRASS = "0"
    ROAD = "1"
    PLAYER = "P"
    BUSH = "B"
    VOID = "X"


Map = List[List[TileKey]]
