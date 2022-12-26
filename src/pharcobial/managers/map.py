from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import MapID, Position, Positional, TileKey
from pharcobial.utils import game_paths, safe_load_csv, to_px


@dataclass
class Map:
    map_id: MapID
    tiles: List[List[TileKey]]
    player_start: Positional | None
    npcs_start: List[Positional]

    @classmethod
    def parse_file(cls, path: Path) -> "Map":
        tiles_lists: List[List[TileKey]] = []
        player_start = None
        npcs_start: List[Positional] = []

        for y, row in enumerate(safe_load_csv(path)):
            tiles: List[TileKey] = []
            for x, tile in enumerate(row):
                key = TileKey(tile)

                match key:
                    case TileKey.PLAYER:
                        player_start = (to_px(x), to_px(y))
                        tiles.append(TileKey.GRASS)
                    case TileKey.BUSH:
                        npcs_start.append((to_px(x), to_px(y)))
                        tiles.append(TileKey.GRASS)
                    case _:
                        # Normal map tile (grass or road)
                        tiles.append(key)

            tiles_lists.append(tiles)

        return cls(
            map_id=path.stem, tiles=tiles_lists, player_start=player_start, npcs_start=npcs_start
        )

    def __iter__(self) -> Iterator[List[TileKey]]:
        yield from self.tiles

    def __getitem__(self, key: int | slice) -> List[TileKey] | List[List[TileKey]]:
        return self.tiles[key]


class MapManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.active: Map | None = None

    @property
    def map_id(self) -> MapID | None:
        if not self.active:
            return None

        return self.active.map_id

    @property
    def player_start(self) -> Positional:
        if not self.active:
            raise ValueError("No map loaded.")

        return self.active.player_start or Position(x=0, y=0)

    @property
    def npcs_start(self) -> List[Positional]:
        if not self.active:
            raise ValueError("No map loaded.")

        return self.active.npcs_start

    def __iter__(self):
        yield from self.active or []

    def __getitem__(self, idx: int | slice):
        return (self.active or [])[idx]

    def load(self, map_id: MapID):
        file_path = game_paths.get_map(map_id)
        self.active = Map.parse_file(file_path)

    def validate(self):
        assert self.player_start
        assert self.active
        game_logger.debug("Map ready.")


map_manager = MapManager()
