import pygame

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction


class Game(BaseManager):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running = False

    def run(self):
        self.setup()
        self.running = True
        while self.running:
            action = self.events.process_next()
            if action == GameAction.QUIT:
                self.running = False
                break

            self.update()
            self.draw()

        pygame.quit()

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
            pygame.display.flip()


def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    main()
