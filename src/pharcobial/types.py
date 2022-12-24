from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Union

from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RETURN, K_RIGHT, K_SPACE, K_UP, KEYDOWN, KEYUP

Color = Tuple[int, int, int]


class InputEvent:
    KEY_DOWN = KEYDOWN
    KEY_UP = KEYUP


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
    MENU = "MENU"


class TileKey(Enum):
    GRASS = "0"
    ROAD = "1"
    PLAYER = "P"
    BUSH = "B"
    VOID = "X"


Map = List[List[TileKey]]


class KeyBinding:
    def __init__(
        self,
        up: int = K_UP,
        down: int = K_DOWN,
        left: int = K_LEFT,
        right: int = K_RIGHT,
        activate: int = K_SPACE,
        escape: int = K_ESCAPE,
        enter: int = K_RETURN,
    ) -> None:
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.activate = activate
        self.escape = escape
        self.enter = enter


@dataclass
class MenuItem:
    index: int
    title: str
