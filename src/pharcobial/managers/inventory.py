from dataclasses import dataclass
from typing import Dict

from pharcobial.managers.base import BaseManager
from pharcobial.types import SpriteID


@dataclass
class InventoryItem:
    name: str
    gfx_id: str
    index: int


class InventoryManager(BaseManager):
    """
    A mapping of investory items by sprite ID.
    """

    items: Dict[SpriteID, Dict[int, InventoryItem]] = {}


inventory_manager = InventoryManager()
