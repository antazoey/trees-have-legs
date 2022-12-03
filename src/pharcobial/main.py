from functools import cached_property

import pygame

from pharcobial.sprites import Edible, Pharma
from pharcobial.utils import Clock, GameDisplay


class App:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        block_size: int = 10,
        fps: int = 20,
        font_size: int = 25,
    ):
        pygame.init()
        self.display = GameDisplay(width, height, block_size, font_size)
        self.clock = Clock(fps)
        self.game_exit = False
        self.game_over = False

    @cached_property
    def player(self):
        return Pharma(self.display)

    @cached_property
    def edible(self):
        return Edible(self.display)

    def main(self):
        while not self.game_exit:
            while self.game_over:
                self.end()

            self.display.clear()
            self.edible.draw()
            for event in pygame.event.get():
                self.player.handle_movement(event)

            self.player.move()
            self.player.draw()
            self.player.eat(self.edible)
            pygame.display.update()
            self.clock.tick()

    def end(self):
        self.turn_off()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_exit = True
                    self.game_over = False
                if event.key == pygame.K_c:
                    run()


def run():
    game = App()
    game.main()
    pygame.quit()


if __name__ == "__main__":
    run()
