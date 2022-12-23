from pathlib import Path
from typing import Dict

from pharcobial.types import Color

BLOCK_SIZE = 32
GAME_NAME = "Pharcobial"

SOURCE_DIR = Path(__file__).parent.parent.parent
GFX_DIR = SOURCE_DIR / "gfx"
MAPS_DIR = SOURCE_DIR / "maps"

DATA_DIRECTORY = Path.home() / f".{GAME_NAME.lower()}"
SAVES_DIRECTORY = DATA_DIRECTORY / "saves"

RGB: Dict[str, Color] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 155, 0),
}
