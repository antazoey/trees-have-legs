from pharcobial.constants import MAPS_DIR
from pharcobial.managers.base import BaseManager
from pharcobial.types import TileKey


class MapManager(BaseManager):
    def __init__(self, map_id: str = "buffer_property") -> None:
        super().__init__()
        self.load(map_id)

    def __iter__(self):
        yield from self.active

    def load(self, map_id: str):
        file_path = MAPS_DIR / f"{map_id}.csv"
        with open(file_path, "r") as file:
            lines = file.readlines()

        self.active = [[TileKey(int(x.strip())) for x in row.split(",")] for row in lines]


map_manager = MapManager()
