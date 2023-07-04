import click

from treeshavelegs.game import Game
from treeshavelegs.options import game_options
from treeshavelegs.types import GameOptions


@click.command("play_thl")
@game_options()
def cli(*args, **kwargs):
    """
    Entry point to the program.
    """

    options = GameOptions(*args, **kwargs)
    game = Game(options)
    game.start()
