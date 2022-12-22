import pygame

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction


class Game(BaseManager):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running = False

    def run(self):
        self.display.validate()
        self.sprites.load()
        self.camera.extend(self.sprites.environment_sprites)
        self.running = True
        while self.running:
            action = self.events.process_next()
            if action == GameAction.QUIT:
                self.running = False
                break

            # Update everything here.
            self.camera.update()

            with self.display.in_same_cycle():
                self.camera.draw()
                pygame.display.flip()

        pygame.quit()


def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    main()
