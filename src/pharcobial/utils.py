import random
import time
from pathlib import Path
from typing import Tuple

from pharcobial.constants import BLOCK_SIZE, SOURCE_DIR


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

    def get_graphic(self, gfx_id: str, ext: str = "png") -> Path:
        return self.gfx / f"{gfx_id}.{ext}"

    def get_map(self, map_id: str) -> Path:
        return self.maps / f"{map_id}.csv"

    def get_font(self, font_name: str) -> Path:
        return self.fonts / f"{font_name}.ttf"


game_paths = GamePaths(SOURCE_DIR)
