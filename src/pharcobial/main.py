import pygame  # type: ignore

from pharcobial._types import GameAction
from pharcobial.managers.base import BaseManager


class Game(BaseManager):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running = False

    def run(self):
        self.display.active.clear()
        self.running = True
        while self.running:
            action = self.events.process_next()
            if action == GameAction.QUIT:
                self.running = False
                break

            self.sprites.update()
            self.sprites.draw()
            self.display.active.update()
            self.clock.tick()

        pygame.quit()


def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    main()
