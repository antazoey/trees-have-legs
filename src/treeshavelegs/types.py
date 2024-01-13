from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Iterator, List, Protocol, Tuple, TypeAlias, Union

from pygame import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RETURN,
    K_RIGHT,
    K_SPACE,
    K_UP,
    KEYDOWN,
    KEYUP,
    Rect,
)

from treeshavelegs.constants import (
    BLOCK_SIZE,
    DEFAULT_FONT_SIZE,
    DEFAULT_FPS,
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
)

if TYPE_CHECKING:
    from treeshavelegs.sprites.base import BaseSprite


Color = Tuple[int, int, int]

SpriteID: TypeAlias = str
GfxID: TypeAlias = str
MapID: TypeAlias = str
SaveID: TypeAlias = str
SfxID: TypeAlias = str
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
    def from_obj(self, obj: Any) -> "Position":
        if hasattr(obj, "rect") and hasattr(obj.rect, "topleft"):
            return Position(*obj.rect.topleft)

        elif isinstance(obj, Rect):
            return Position(*obj.topleft)

        return Position(*obj)

    @classmethod
    def parse_coordinates(cls, x: float, y: float) -> "Position":
        return cls(x=x * BLOCK_SIZE, y=y * BLOCK_SIZE)


Positional = Union[Tuple[float, float], Position]


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
        one: int = K_1,
        two: int = K_2,
        three: int = K_3,
        four: int = K_4,
        five: int = K_5,
        six: int = K_6,
        seven: int = K_7,
        eight: int = K_8,
        nine: int = K_9,
    ) -> None:
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.activate = activate
        self.escape = escape
        self.enter = enter
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five
        self.six = six
        self.seven = seven
        self.eight = eight
        self.nine = nine

    @property
    def movement(self) -> Tuple[int, int, int, int]:
        return (self.left, self.right, self.up, self.down)

    @property
    def inventory(self) -> Tuple[int, int, int, int, int, int, int, int, int]:
        return (
            self.one,
            self.two,
            self.three,
            self.four,
            self.five,
            self.six,
            self.seven,
            self.eight,
            self.nine,
        )

    def number_key_to_int(self, number_key: int) -> int:
        return self.inventory.index(number_key)


@dataclass
class MenuItem:
    title: str
    index: int
    action: Callable


class WorldStage:
    FIND_FRIEND_CARD = 0
    GET_TAYLOR_BACK = 1
    GET_LESTER_BACK = 2
    END = 3

    def __len__(self) -> int:
        return self.END

    @classmethod
    def next(cls, previous: int) -> int:
        if previous < 0:
            return cls.FIND_FRIEND_CARD

        elif previous < cls.END:
            return previous + 1

        else:
            return cls.END


@dataclass
class GameOptions:
    # Core settings
    window_width: int = DEFAULT_WIDTH
    window_height: int = DEFAULT_HEIGHT
    fps: int = DEFAULT_FPS
    font_size: int = DEFAULT_FONT_SIZE
    full_screen: bool = False
    raise_exceptions: bool = False

    # Game settings
    save_id: SaveID | None = None  # Set when loading a saved game.
    """Load a saved game. Mutually exclusive with ``map_id``."""

    # Debug
    debug: bool = False

    # Audio settings
    disable_music: bool = False
    disable_sfx: bool = False

    stage: int = WorldStage.FIND_FRIEND_CARD

    def __post_init__(self):
        # Ensure options are valid.
        if self.save_id is not None:
            if self.stage is not None:
                raise ValueError("Cannot set both stage and save IDs.")

        elif self.stage is None:
            # Both save and stage are None. Load start.
            self.stage = 0

    def __setitem__(self, key: str, val: Any):
        setattr(self, key, val)


class Visible(Protocol):
    visible: bool


@dataclass
class Collision:
    x: Union["BaseSprite", None] = None
    y: Union["BaseSprite", None] = None


Locatable = Union[Rect, "BaseSprite", Positional]


@dataclass
class InventoryItem:
    name: str
    gfx_id: str
    index: int
