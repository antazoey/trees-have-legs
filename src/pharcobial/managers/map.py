from pharcobial.constants import MAPS_DIR
from pharcobial.managers.base import BaseManager
from pharcobial.types import Map, TileKey


class MapManager(BaseManager):
    active: str = "buffer_property"

    def __iter__(self):
        yield from self[self.active]

    def __getitem__(self, map_id: str) -> Map:
        file_path = MAPS_DIR / f"{map_id}.csv"
        with open(file_path, "r") as file:
            lines = file.readlines()

        return [[TileKey(int(x.strip())) for x in row.split(",")] for row in lines]


map_manager = MapManager()
