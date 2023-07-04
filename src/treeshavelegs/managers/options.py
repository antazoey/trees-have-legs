from typing import Any

from treeshavelegs.logging import game_logger
from treeshavelegs.managers.base import BaseManager
from treeshavelegs.types import GameOptions, KeyBinding


class OptionsManager(BaseManager):
    key_bindings: KeyBinding = KeyBinding()
    loaded: GameOptions | None = None

    def load(self, options: GameOptions):
        self.loaded = options

    def __getattr__(self, key: str) -> Any:
        return self[key]

    def __setitem__(self, key: str, value: Any):
        if not self.loaded:
            raise ValueError("Options are not loaded.")

        self.loaded[key] = value

    def __getitem__(self, key: str) -> Any:
        """
        Prevents us from having to do
        ``self.options.loaded`` and makes ``self.options`` work.
        """

        main_err = None
        try:
            return self.__getattribute__(key)
        except AttributeError as err:
            main_err = err

        # Check if from options.
        try:
            return getattr(self.loaded, key)
        except Exception:
            if main_err is not None:
                raise main_err

            raise  # err_backup

    def validate(self):
        assert self.loaded is not None
        game_logger.debug("Options ready.")


options_manager = OptionsManager()
