import random
import sys
import time
from pathlib import Path
from typing import Callable, List, Tuple

import pygame

from pharcobial.constants import BLOCK_SIZE, SOURCE_DIR
from pharcobial.types import FontName, GfxID, MapID


def chance(odds: Tuple[int, int]) -> bool:
    """
    Give it odds, like [5, 6] meaning (5/6), and it will tell
    you if you randomly achieved those odds.
    """

    # Use salt to throw off random algorithm.
    salt = round(time.time()) & 7 + 3
    random.randint(0, salt)

    must, total = odds
    must *= 100
    total *= 100
    res = random.randint(0, total)
    return res <= must


def to_px(val: int) -> int:
    """
    Convert block size to pixels.
    """
    return val * BLOCK_SIZE


class GamePaths:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    @property
    def gfx(self) -> Path:
        return self.base_dir / "gfx"

    @property
    def maps(self) -> Path:
        return self.base_dir / "maps"

    @property
    def fonts(self) -> Path:
        return self.base_dir / "fonts"

    def get_graphic(self, gfx_id: GfxID, ext: str = "png") -> Path:
        return self.gfx / f"{gfx_id}.{ext}"

    def get_map(self, map_id: MapID) -> Path:
        return self.maps / f"{map_id}.csv"

    def get_font(self, font_name: FontName) -> Path:
        return self.fonts / f"{font_name}.ttf"


def quit():
    pygame.quit()
    sys.exit()


game_paths = GamePaths(SOURCE_DIR)


def safe_load_csv(path: Path, cb: Callable = str) -> List[List]:
    if not path.is_file():
        return []

    rows: List[List] = []
    with open(path, "r") as file:
        lines = file.readlines()

    for line in lines:
        row: List = [cb(x.strip()) for x in line.split(",")]
        rows.append(row)

    return rows
