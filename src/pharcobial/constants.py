import os
from pathlib import Path
from typing import Dict

from pharcobial.types import Color

NAME = str(__file__).split(os.path.sep)[0].replace(".py", "").capitalize()
BLOCK_SIZE = 32
SOURCE_DIR = Path(__file__).parent.parent.parent
MAPS_DIR = SOURCE_DIR / "maps"
GFX_DIR = SOURCE_DIR / "gfx"
RGB: Dict[str, Color] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 155, 0),
}
