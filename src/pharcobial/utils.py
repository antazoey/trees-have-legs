import random
import time
from typing import Tuple


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
