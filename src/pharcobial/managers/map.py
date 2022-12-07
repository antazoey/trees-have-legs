from enum import Enum


class Key(Enum):
    GRASS = 0


class Map:
    def __init__(self, width: int = 1_000, height: int = 1_000) -> None:
        self.width = width  # Blocks
        self.height = height  # Blocks

        # TODO: Add more tiles besides grass.
        self.cells = [[Key.GRASS for _ in range(self.width)] for _ in range(self.height)]


class MapManager:
    active_map = Map()


map_manager = MapManager()
