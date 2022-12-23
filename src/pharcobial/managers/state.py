from pathlib import Path
from typing import Dict, Iterable

from pharcobial.constants import SAVES_DIRECTORY
from pharcobial.managers.base import BaseManager


class StateManager(BaseManager):
    """
    Responsible for saving and loading.
    """

    def saves(self) -> Iterable[Path]:
        for x in SAVES_DIRECTORY.iterdir():
            if x.is_file() and x.suffix == ".json":
                yield x

    @property
    def num_saves(self) -> int:
        return len(list(self.saves()))

    def dict(self) -> Dict:
        """
        The entire game state.
        """

        return {"sprites": self.sprites.dict()}


state_manager = StateManager()
