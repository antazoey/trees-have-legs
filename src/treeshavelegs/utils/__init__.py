import random
import sys
import time
from typing import Tuple

import pygame

from treeshavelegs.constants import BLOCK_SIZE


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


def quit():
    pygame.quit()
    sys.exit()


def noop(*args, **kwargs):
    pass
