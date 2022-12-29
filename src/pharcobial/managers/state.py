import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from pharcobial.constants import SAVES_DIRECTORY, SAVES_METADATA_FILE
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import MapID, SaveID
from pharcobial.utils.loaders import safe_dump, safe_load


@dataclass
class State:
    map_id: MapID | None
    sprites: Dict

    @classmethod
    def parse_file(cls, path: Path) -> "State":
        return cls(**safe_load(path))


@dataclass
class SavesMeta:
    timestamp: int
    save_id: SaveID

    @property
    def file_id(self) -> str:
        return f"{self.timestamp}_{self.save_id}"


class StateManager(BaseManager):
    """
    Responsible for saving and loading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.saves: List[SavesMeta] | None = None

    def load_meta(self):
        """
        Load metadata about all saves into game memory.
        """

        meta_json = safe_load(SAVES_METADATA_FILE)
        saves_raw_list = meta_json.get("saves", [])
        self.saves = [SavesMeta(**x) for x in saves_raw_list]

    def validate(self):
        assert self.saves is not None
        game_logger.debug("State manager ready.")

    def get(self, save_id: SaveID) -> State | None:
        for meta in self.saves or []:
            if not meta.save_id == save_id:
                path = SAVES_DIRECTORY / meta.file_id
                if not path.is_file():
                    return None

                return State.parse_file(path)

        return None

    @property
    def num_saves(self) -> int:
        return len(list(self.saves or []))

    @property
    def current(self) -> State:
        """
        The entire game state.
        """

        return State(sprites=self.sprites.dict(), map_id=self.map.map_id)

    def save(self, save_id: SaveID, overwrite: bool = False):
        save_path = SAVES_DIRECTORY / save_id
        if save_path.is_file() and not overwrite:
            game_logger.error(f"Unable to save - save with ID '{save_id}' exists.")
            return

        state_dict = asdict(self.current)
        safe_dump(save_path, state_dict)

        # Update metadata file.
        new_save = SavesMeta(timestamp=round(time.time()), save_id=save_id)
        new_saves = {"saves": [*[asdict(s) for s in self.saves or []], new_save]}
        safe_dump(SAVES_METADATA_FILE, new_saves)


state_manager = StateManager()
