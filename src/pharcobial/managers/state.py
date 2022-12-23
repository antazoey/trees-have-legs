from typing import Dict
from pathlib import Path

from pharcobial.constants import GAME_NAME
from pharcobial.managers.base import BaseManager


class StateManager(BaseManager):
    """
    Responsible for saving and loading.
    """

    def dict(self) -> Dict:
        """
        The entire game state.
        """

        return {"sprites": self.sprites.dict()}
        


state_manager = StateManager()
