from traceback import format_exc

import pygame

from treeshavelegs.logging import game_logger
from treeshavelegs.managers.base import ManagerAccess
from treeshavelegs.types import GameEvent, GameOptions
from treeshavelegs.utils import quit


class Game(ManagerAccess):
    def __init__(self, game_options: GameOptions):
        super().__init__()
        pygame.init()
        self.running = False
        self.options.load(game_options)

    def start(self):
        """
        Start the game.
        Does game setup and then runs the game
        """
        self.setup()
        self.run()
        quit()

    def setup(self):
        """
        All initial game setup happens here.
        If starting from beginning of the game, load initial setup.
        Else, load from a saved state.
        """

        # Validate is used to ensure the creation of a dependency
        # before other logic. This is to help the dependency injection
        # have some ordering, as needed.
        for manager in (
            self.options,
            self.display,
            self.map,
            self.world,
            self.collision,
        ):
            manager.validate()

        # Load all sprites in this level.
        self.sprites.create_sprites()
        self.sprites.validate()

        # Have the camera follow the player initially.
        self.world.follow(self.sprites.player)

        # Start off in normal, world mode.
        self.views.goto(self.world)

    def run(self):
        """
        Runs the game. Controls the game loop.
        """
        self.running = True
        while self.running:
            try:
                self.react()
            except Exception as err:
                if self.options.raise_exceptions:
                    raise  # Raise this exception
                else:
                    game_logger.error(format_exc())

    def react(self):
        """
        React to game events.
        """

        for event in self.events.queue:
            match event:
                case GameEvent.QUIT:
                    self.running = False
                    quit()

                case GameEvent.MENU:
                    self.clock.paused = True
                    self.views.goto(self.menu)
                    self.views.active.run()

                case GameEvent.CONTINUE:
                    self.views.active.run()
