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

            # Update everything here.
            self.map.update()
            self.sprites.update()

            with self.display.in_same_cycle():
                self.map.draw()
                self.sprites.draw()
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
