import sys

import pygame

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction


class Game(BaseManager):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running = False
        self.paused = False

    def run(self):
        self.setup()
        self.running = True
        while self.running:

            action = self.events.process_next()

            match action:
                case GameAction.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                case GameAction.MENU:
                    self.paused = not self.paused
                    if self.paused:
                        self.display.show_text(
                            "Paused", self.display.half_width, self.display.half_height, "red"
                        )
                        self.display.tick()

                case GameAction.CONTINUE:
                    if not self.paused:
                        self.update()
                        self.draw()

    def setup(self):
        # Validate is used to ensure the creation of a dependency
        # before other logic. This is to help the dependency injection
        # have some ordering, as needed.
        for manager in (
            self.options,
            self.display,
            self.map,
            self.camera,
            self.collision,
        ):
            manager.validate()
        # Load all sprites in this level.
        self.sprites.init_sprites()
        self.sprites.validate()

        # Set the camera to follow the player. This must happen after loading sprites.
        self.camera.followee = self.sprites.player

    def update(self):
        # Update everything here.
        self.camera.update()

    def draw(self):
        with self.display.in_same_cycle():
            self.camera.draw()


def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    main()
