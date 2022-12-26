from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Tuple

from pharcobial.constants import MAP_VOID
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import GfxID, MapID, Position, Positional, SpriteID, TileKey
from pharcobial.utils import game_paths, safe_load, safe_load_csv


@dataclass
class MapCharacterData:
    sprite_id: SpriteID
    location: Position

    @classmethod
    def parse_obj(cls, obj: Dict) -> "MapCharacterData":
        location = Position.parse_coordinates(**obj["location"])
        return cls(sprite_id=obj["sprite_id"], location=location)


@dataclass
class MapMetaData:
    map_id: MapID
    tile_set: Dict[TileKey, GfxID]
    player: MapCharacterData
    npcs: List[MapCharacterData]

    @classmethod
    def parse_file(cls, path: Path) -> "MapMetaData":
        data = safe_load(path)
        data["player"] = MapCharacterData.parse_obj(data["player"])
        data["npcs"] = [MapCharacterData.parse_obj(npc) for npc in data.get("npcs", [])]
        return cls(**data)


@dataclass
class Map:
    map_id: MapID
    metadata: MapMetaData
    tiles: List[List[TileKey]]

    @classmethod
    def parse_file(cls, path: Path) -> "Map":
        metadata_file = path.parent / f"{path.stem}.json"
        metadata = MapMetaData.parse_file(metadata_file)
        tiles_lists: List[List[TileKey]] = []

        for row in safe_load_csv(path):
            tiles: List[TileKey] = []
            for tile in row:
                tiles.append(tile)

            tiles_lists.append(tiles)

        return cls(map_id=path.stem, tiles=tiles_lists, metadata=metadata)

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

        return self.active.metadata.player.location

    @property
    def npcs_start(self) -> Iterator[Tuple[SpriteID, Positional]]:
        if not self.active:
            raise ValueError("No map loaded.")

        for npc in self.active.metadata.npcs:
            yield npc.sprite_id, npc.location

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

    def get_tile_info(self, tile_key: str) -> Tuple[GfxID | None, Positional]:
        active = self.active
        if tile_key == MAP_VOID or not active:
            return None, (0, -10)

        gfx_id = active.metadata.tile_set[tile_key]
        return gfx_id, (0, 0)


map_manager = MapManager()
