import argparse
from dataclasses import dataclass


@dataclass
class GameOptions:
    # Core settings
    width: int = 800
    height: int = 600
    fps: int = 60
    font_size: int = 25

    # Game settings
    num_monsters: int = 3


def get_game_options():
    """
    Game options are read in from the CLI.
    """
    parser = argparse.ArgumentParser()

    # Add core settings
    parser.add_argument("--width", action="store", default=800, help="Window width")
    parser.add_argument("--height", action="store", default=600, help="Window height")
    parser.add_argument("--fps", action="store", default=60, help="Frames per second")
    parser.add_argument("--font-size", action="store", default=25, help="Font size")

    # Add game settings
    parser.add_argument(
        "--num-monsters", action="store", default=3, help="The number of monster chasing you."
    )

    parsed_args = parser.parse_args()

    return GameOptions(
        width=int(parsed_args.width),
        height=int(parsed_args.height),
        fps=int(parsed_args.fps),
        font_size=int(parsed_args.font_size),
        num_monsters=int(parsed_args.num_monsters),
    )
