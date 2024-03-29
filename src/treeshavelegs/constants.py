from pathlib import Path
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from treeshavelegs.types import Color, GfxID, MapID


BLOCK_SIZE = 32
GAME_NAME = "Trees Have Legs"

SOURCE_DIR = Path(__file__).parent.parent.parent
DATA_DIRECTORY = Path.home() / f".{GAME_NAME.lower()}"
SAVES_DIRECTORY = DATA_DIRECTORY / "saves"
SAVES_METADATA_FILE = DATA_DIRECTORY / "saves_meta.json"

RGB: Dict[str, "Color"] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "onyx": (0, 0, 26),
    "red": (153, 25, 0),
    "green": (0, 155, 0),
    "blue": (0, 51, 77),
    "gold": (230, 153, 0),
}


class Maps:
    FIRE_PIT: "MapID" = "fire_pit"
    BUFFER_PROPERTY: "MapID" = "buffer_property"


class Graphics:
    TREE: "GfxID" = "tree"
    CHAT_BUBBLE: "GfxID" = "chat-bubble"
    JULES: "GfxID" = "jules"
    TAYLOR: "GfxID" = "taylor"


class Views:
    WORLD = "world"
    MENU = "menu"  # Wrapper
    MAIN_MENU = "main-menu"
    OPTIONS_MENU = "options-menu"


# Default settings
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800
DEFAULT_FPS = 32
DEFAULT_FONT_SIZE = 25

# Default attributes
DEFAULT_HP = 100
DEFAULT_MAX_HP = 100
DEFAULT_AP = 1

MAP_VOID = "X"
VOID_POS = (-69, -420)
