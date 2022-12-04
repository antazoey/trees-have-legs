from functools import cached_property
from typing import List

import pygame

from pharcobial.sprites import Monster, Player
from pharcobial.utils import Clock, GameDisplay


class App:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        fps: int = 20,
        font_size: int = 25,
        num_monsters: int = 3,
    ):
        pygame.init()
        self.display = GameDisplay(width, height, font_size)
        self.clock = Clock(fps)
        self.game_exit = False
        self.num_monsters = num_monsters

    @cached_property
    def player(self) -> Player:
        return Player(self.display)

    @cached_property
    def monsters(self) -> List[Monster]:
        return [Monster(self.display) for _ in range(self.num_monsters)]

    def main(self):
        self.display.clear()
        while not self.game_exit:
            for event in pygame.event.get():
                self.player.handle_event(event)

            self.player.move()
            self.draw()

            pygame.display.update()
            self.clock.tick()

    def draw(self):
        self.player.draw()

        for monster in self.monsters:
            monster.draw()


def run():
    game = App()
    game.main()
    pygame.quit()


if __name__ == "__main__":
    run()
