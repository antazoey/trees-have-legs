from pathlib import Path
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pharcobial.types import Color, GfxID, MapID


BLOCK_SIZE = 32
GAME_NAME = "Pharcobial"

SOURCE_DIR = Path(__file__).parent.parent.parent
DATA_DIRECTORY = Path.home() / f".{GAME_NAME.lower()}"
SAVES_DIRECTORY = DATA_DIRECTORY / "saves"
SAVES_METADATA_FILE = DATA_DIRECTORY / "saves_meta.json"

RGB: Dict[str, "Color"] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (150, 0, 0),
    "green": (0, 155, 0),
}


class Maps:
    BUFFER_PROPERTY: "MapID" = "buffer_property"


class Graphics:
    CHAT_BUBBLE: "GfxID" = "chat-bubble"


# Default settings
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800
DEFAULT_FPS = 60
DEFAULT_FONT_SIZE = 25
DEFAULT_MAP = Maps.BUFFER_PROPERTY
