from dataclasses import dataclass
from enum import Enum
from typing import Iterator, List, Tuple, TypeAlias, Union

from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RETURN, K_RIGHT, K_SPACE, K_UP, KEYDOWN, KEYUP

from pharcobial.constants import (
    BLOCK_SIZE,
    DEFAULT_FONT_SIZE,
    DEFAULT_FPS,
    DEFAULT_HEIGHT,
    DEFAULT_MAP,
    DEFAULT_WIDTH,
)

Color = Tuple[int, int, int]

SpriteID: TypeAlias = str
GfxID: TypeAlias = str
MapID: TypeAlias = str
SaveID: TypeAlias = str
FontName: TypeAlias = str
TileKey: TypeAlias = str


class UserInput:
    KEY_DOWN = KEYDOWN
    KEY_UP = KEYUP


class Position(tuple):
    def __new__(cls, *args, **kwargs) -> "Position":
        x_and_y = tuple(args)
        if not x_and_y:
            x_and_y = tuple(kwargs.values())

        return super().__new__(cls, x_and_y)

    def __init__(self, x: Union[float, "Positional"], y: float | None = None) -> None:
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x = x
            self.y = y
        elif isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]

        super().__init__()

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    @classmethod
    def parse_coordinates(cls, x: float, y: float) -> "Position":
        return cls(x=x * BLOCK_SIZE, y=y * BLOCK_SIZE)


Positional = Tuple[float, float] | Position


class GameEvent(Enum):
    """
    An action the root Game should take, based on the event processor.
    """

    QUIT = "QUIT"
    CONTINUE = "CONTINUE"
    MENU = "MENU"


Map = List[List[TileKey]]


class KeyBinding:
    def __init__(
        self,
        left: int = K_LEFT,
        right: int = K_RIGHT,
        up: int = K_UP,
        down: int = K_DOWN,
        activate: int = K_SPACE,
        escape: int = K_ESCAPE,
        enter: int = K_RETURN,
    ) -> None:
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.activate = activate
        self.escape = escape
        self.enter = enter

    @property
    def movement(self) -> Tuple[int, int, int, int]:
        return (self.left, self.right, self.up, self.down)


@dataclass
class MenuItem:
    index: int
    title: str


@dataclass
class GameOptions:
    # Core settings
    window_width: int = DEFAULT_WIDTH
    window_height: int = DEFAULT_HEIGHT
    fps: int = DEFAULT_FPS
    font_size: int = DEFAULT_FONT_SIZE
    full_screen: bool = False

    # Game settings
    map_id: MapID = DEFAULT_MAP
    """Load a particular map from start."""

    save_id: SaveID | None = None  # Set when loading a saved game.
    """Load a saved game. Mutually exclusive with ``map_id``."""

    # Debug
    debug: bool = False

    def __post_init__(self):
        # Ensure options are valid.
        if self.save_id is not None:
            if self.map_id is not None:
                raise ValueError("Cannot set both map and save IDs.")

        elif self.map_id is None:
            # Both save and map are None. Load default map.
            self.map_id = DEFAULT_MAP
