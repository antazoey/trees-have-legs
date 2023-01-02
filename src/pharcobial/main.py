import click

from pharcobial.game import Game
from pharcobial.options import game_options
from pharcobial.types import GameOptions


@click.command("play_pharcobial")
@game_options()
def cli(*args, **kwargs):
    """
    Entry point to the program.
    """

    options = GameOptions(*args, **kwargs)
    game = Game(options)
    game.start()
