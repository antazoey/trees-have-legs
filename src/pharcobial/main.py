import click

from pharcobial.game import Game
from pharcobial.options import game_options
from pharcobial.types import GameOptions


@click.command("play_pharcobial")
@game_options()
def cli(window_width, window_height, fps, font_size, full_screen, debug, map_id, save_id):
    """
    Entry point to the program.
    """

    options = GameOptions(
        window_width=window_width,
        window_height=window_height,
        fps=fps,
        font_size=font_size,
        full_screen=full_screen,
        debug=debug,
        map_id=map_id,
        save_id=save_id,
    )
    game = Game(options)
    game.run()
