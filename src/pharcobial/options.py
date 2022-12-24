from logging import DEBUG

import click

from pharcobial.constants import (
    DEFAULT_FONT_SIZE,
    DEFAULT_FPS,
    DEFAULT_HEIGHT,
    DEFAULT_MAP,
    DEFAULT_WIDTH,
)
from pharcobial.logging import game_logger


def window_width():
    return click.option("--window-width", default=DEFAULT_WIDTH, help="Window width", type=int)


def window_height():
    return click.option("--window-height", default=DEFAULT_HEIGHT, help="Window height", type=int)


def fps_option():
    return click.option("--fps", default=DEFAULT_FPS, help="Frames per second", type=int)


def font_size():
    return click.option(
        "--font-size", default=DEFAULT_FONT_SIZE, help="Numeric font size", type=int
    )


def full_screen():
    return click.option("--full-screen", is_flag=True, help="Play in full screen mode.")


def debug():
    def cb(ctx, param, value):
        if value:
            # Set DEBUG logger ASAP in arg parsing process to ensure capturing logs.
            game_logger.setLevel(DEBUG)

        return value

    return click.option("--debug", is_flag=True, help="Play in full screen mode.", callback=cb)


def map_id():
    return click.option("--map", "map_id", default=DEFAULT_MAP, help="The name of the map to load.")


def save_id():
    return click.option("--load", "save_id", help="A load a saved game by ID.")


def game_options():
    def fn(f):
        f = window_width()(f)
        f = window_height()(f)
        f = fps_option()(f)
        f = font_size()(f)
        f = full_screen()(f)
        f = debug()(f)
        f = map_id()(f)
        f = save_id()(f)
        return f

    return fn
