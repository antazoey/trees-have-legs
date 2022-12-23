import argparse
from dataclasses import dataclass
from functools import cached_property
from logging import DEBUG
from typing import Any

from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import KeyBinding

DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800
DEFAULT_FPS = 60
DEFAULT_FONT_SIZE = 25
DEFAULT_FULL_SCREEN = False


@dataclass
class GameOptions:
    # Core settings
    window_width: int = DEFAULT_WIDTH
    window_height: int = DEFAULT_HEIGHT
    fps: int = DEFAULT_FPS
    font_size: int = DEFAULT_FONT_SIZE
    full_screen: bool = DEFAULT_FULL_SCREEN

    # Debug
    debug: bool = False


class OptionsManager(BaseManager):

    key_bindings: KeyBinding = KeyBinding()

    @cached_property
    def options(self):
        """
        Game options are read in from the CLI.
        """

        parser = argparse.ArgumentParser()

        # Add core settings
        parser.add_argument(
            "--window-width", action="store", default=DEFAULT_WIDTH, help="Window width", type=int
        )
        parser.add_argument(
            "--window-height",
            action="store",
            default=DEFAULT_HEIGHT,
            help="Window height",
            type=int,
        )
        parser.add_argument(
            "--fps", action="store", default=DEFAULT_FPS, help="Frames per second", type=int
        )
        parser.add_argument(
            "--font-size", action="store", default=DEFAULT_FONT_SIZE, help="Font size", type=int
        )
        parser.add_argument(
            "--full-screen", action="store_true", default=DEFAULT_FULL_SCREEN, help="Full screen"
        )
        parser.add_argument("--debug", action="store_true", help="Set to enable DEBUG logging.")

        parsed_args = parser.parse_args()

        # Set DEBUG logger ASAP in arg parsing process to ensure capturing logs.
        if parsed_args.debug:
            game_logger.setLevel(DEBUG)

        return GameOptions(
            window_width=parsed_args.window_width,
            window_height=parsed_args.window_height,
            fps=parsed_args.fps,
            font_size=parsed_args.font_size,
            full_screen=parsed_args.full_screen,
            debug=parsed_args.debug,
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

    def validate(self):
        assert self.options is not None
        game_logger.debug("Options ready.")


options_manager = OptionsManager()
