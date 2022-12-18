from enum import Enum

from pygame.surface import Surface  # type: ignore

from pharcobial.constants import BLOCK_SIZE

from .base import BaseManager


class Key(Enum):
    GRASS = "grass"
    ROAD = "road"


class Map:
    def __init__(self, width: int = 1000, height: int = 1000) -> None:
        self.width = width  # Blocks
        self.height = height  # Blocks
        self.rows = []

        # Create full map (not just what is displayed)
        rows = []
        for y in range(self.width):
            row = []

            for x in range(self.height):

                if x == 300:
                    key = Key.ROAD
                else:
                    key = Key.GRASS

                row.append(key)

            rows.append(row)

        self.rows = rows


class MapManager(BaseManager):
    active_map = Map()

    pointer: int = 0
    """
    The pointer to the top left corner of the section of the map
    that is visible.
    """

    def get_visible_cells(self):
        player = self.sprites.player.coordinates
        half_map_x = self.display.width // BLOCK_SIZE // 2
        half_map_y = self.display.height // BLOCK_SIZE // 2
        start_x = player.x - half_map_x
        end_x = player.x + half_map_x
        start_y = player.y - half_map_y
        end_y = player.y + half_map_y
        return [r[start_x:end_x] for r in self.active_map.rows[start_y:end_y]]

    def update(self):
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
