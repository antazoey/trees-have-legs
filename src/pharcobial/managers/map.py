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

        if MAP_VOID not in data["tile_set"]:
            data["tile_set"][MAP_VOID] = None

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
        tiles = safe_load_csv(path)
        return cls(map_id=path.stem, tiles=tiles, metadata=metadata)

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
            # Shouldn't really happen.
            return Position(x=0, y=0)

        return self.active.metadata.player.location

    @property
    def npcs_start(self) -> Iterator[Tuple[SpriteID, Positional]]:
        if not self.active:
            return

        for npc in self.active.metadata.npcs:
            yield npc.sprite_id, npc.location

    @property
    def tile_set(self) -> Dict[TileKey, GfxID]:
        if not self.active:
            return {}

        return self.active.metadata.tile_set

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
