import argparse
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from .base import BaseManager


@dataclass
class GameOptions:
    # Core settings
    window_width: int = 800
    window_height: int = 600
    fps: int = 60
    font_size: int = 25
    full_screen: bool = False

    # Game settings
    num_monsters: int = 3


class OptionsParser(BaseManager):
    @cached_property
    def options(self):
        """
        Game options are read in from the CLI.
        """

        parser = argparse.ArgumentParser()

        # Add core settings
        parser.add_argument(
            "--window-width", action="store", default=800, help="Window width", type=int
        )
        parser.add_argument(
            "--window-height", action="store", default=600, help="Window height", type=int
        )
        parser.add_argument("--fps", action="store", default=60, help="Frames per second", type=int)
        parser.add_argument("--font-size", action="store", default=25, help="Font size", type=int)
        parser.add_argument("--full-screen", action="store_true", default=False, help="Full screen")

        # Add game settings
        parser.add_argument(
            "--num-monsters",
            action="store",
            default=3,
            help="The number of monster chasing you.",
            type=int,
        )

        parsed_args = parser.parse_args()

        return GameOptions(
            window_width=parsed_args.window_width,
            window_height=parsed_args.window_height,
            fps=parsed_args.fps,
            font_size=parsed_args.font_size,
            full_screen=parsed_args.full_screen,
            num_monsters=parsed_args.num_monsters,
        )

    def __getattr__(self, key: str) -> Any:
        """
        Prevents us from having to do
        ``self.options.options`` and makes ``self.options`` work.
        """

        main_err = None
        try:
            return self.__getattribute__(key)
        except AttributeError as err:
            main_err = err

        # Check if from options.
        try:
            return getattr(self.options, key)
        except Exception:
            if main_err is not None:
                raise main_err

            raise  # err_backup


options_parser = OptionsParser()
