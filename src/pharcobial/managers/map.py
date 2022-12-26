from typing import List

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import MapID, Positional, TileKey
from pharcobial.utils import game_paths, to_px


class MapManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.player_start: Positional | None = None
        self.bushes_start: List[Positional] = []
        self.active: List[List[TileKey]] = []

    def __iter__(self):
        yield from self.active

    def __getitem__(self, idx: int | slice):
        return self.active[idx]

    def load(self, map_id: MapID):
        file_path = game_paths.get_map(map_id)
        with open(file_path, "r") as file:
            lines = file.readlines()

        for y, row in enumerate(lines):
            row_tiles: List[TileKey] = []
            for x, tile in enumerate(row.split(",")):
                key = TileKey(tile.strip())

                match key:
                    case TileKey.PLAYER:
                        self.player_start = (to_px(x), to_px(y))
                        row_tiles.append(TileKey.GRASS)
                    case TileKey.BUSH:
                        self.bushes_start.append((to_px(x), to_px(y)))
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
