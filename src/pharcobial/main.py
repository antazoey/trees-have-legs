import pygame

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction
from pharcobial.utils import quit


class Game(BaseManager):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running = False

    def run(self):
        self.setup()
        self.running = True
        while self.running:
            self._run()

    def _run(self):
        action = self.events.process()

        match action:
            case GameAction.QUIT:
                self.running = False
                quit()

            case GameAction.MENU:
                self.clock.paused = not self.clock.paused
                self.menu.visible = self.clock.paused
                if self.menu.visible:
                    with self.display.in_same_cycle():
                        self.menu.draw()

            case GameAction.CONTINUE:
                manager: BaseManager
                if self.clock.paused:
                    manager = self.menu
                else:
                    manager = self.camera
                    self.camera.update()

                with self.display.in_same_cycle():
                    manager.draw()

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


def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
