from typing import List

from pharcobial.constants import BLOCK_SIZE, MAPS_DIR
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import Position, TileKey


class MapManager(BaseManager):
    def __init__(self, map_id: str = "buffer_property") -> None:
        super().__init__()
        self.player_start: Position | None = None
        self.bushes_start: List[Position] = []
        self.active: List[List[TileKey]] = []
        self.load(map_id)

    def __iter__(self):
        yield from self.active

    def load(self, map_id: str):
        file_path = MAPS_DIR / f"{map_id}.csv"
        with open(file_path, "r") as file:
            lines = file.readlines()

        for y, row in enumerate(lines):
            row_tiles: List[TileKey] = []
            for x, tile in enumerate(row.split(",")):
                key = TileKey(tile.strip())

                match key:
                    case TileKey.PLAYER:
                        self.player_start = Position(x * BLOCK_SIZE, y * BLOCK_SIZE)
                        row_tiles.append(TileKey.GRASS)
                    case TileKey.BUSH:
                        self.bushes_start.append(Position(x * BLOCK_SIZE, y * BLOCK_SIZE))
                        row_tiles.append(TileKey.GRASS)
                    case _:
                        # Normal map tile (grass or road)
                        row_tiles.append(key)

            self.active.append(row_tiles)

    def validate(self):
        assert self.player_start
        assert self.active
        game_logger.debug("Map ready.")


map_manager = MapManager()
