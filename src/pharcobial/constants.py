import os
from pathlib import Path

NAME = str(__file__).split(os.path.sep)[0].replace(".py", "").capitalize()
BLOCK_SIZE = 16
SOURCE_DIR = Path(__file__).parent.parent.parent
MAPS_DIR = SOURCE_DIR / "maps"
