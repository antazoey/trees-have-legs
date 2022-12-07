from enum import Enum

from pygame.surface import Surface  # type: ignore

from pharcobial.constants import BLOCK_SIZE

from .base import BaseManager


class Key(Enum):
    GRASS = "grass"


class Map:
    def __init__(self, width: int = 1_000, height: int = 1_000) -> None:
        self.width = width  # Blocks
        self.height = height  # Blocks

        # TODO: Add more tiles besides grass.
        self.rows = [[Key.GRASS for _ in range(self.width)] for _ in range(self.height)]


class MapManager(BaseManager):
    active_map = Map()

    pointer: int = 0
    """
    The pointer to the top left corner of the section of the map
    that is visible.
    """

    def get_visible_cells(self):
        return [
            r[: self.display.width // BLOCK_SIZE]
            for r in self.active_map.rows[: self.display.height // BLOCK_SIZE]
        ]

    def update(self):
        # TODO
        pass

    def draw(self):
        map = Surface((self.display.width, self.display.height))
        cells = self.get_visible_cells()
        for y_index, row in enumerate(cells):
            for x_index, tile in enumerate(row):
                image = self.images[tile.value]
                map.blit(image, (x_index * BLOCK_SIZE, y_index * BLOCK_SIZE))

        self.display.active.draw_surface(map)


map_manager = MapManager()
