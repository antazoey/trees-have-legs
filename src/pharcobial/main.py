from functools import cached_property
from typing import List

import pygame

from pharcobial.display import GameDisplay
from pharcobial.monster import Monster
from pharcobial.motion import MotionGranter
from pharcobial.player import Player


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self.fps = fps

    def tick(self):
        self._clock.tick(self.fps)


class Game:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        fps: int = 60,
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
        return Player(self.display, self.motion_granter)

    @cached_property
    def monsters(self) -> List[Monster]:
        return [
            Monster(self.display, self.motion_granter, index) for index in range(self.num_monsters)
        ]

    @cached_property
    def motion_granter(self) -> MotionGranter:
        return MotionGranter(self.display)

    def main(self):
        self.display.clear()
        while not self.game_exit:
            self.update_player()
            self.update_monsters()
            self.draw()
            pygame.display.update()
            self.clock.tick()

    def update_player(self):
        for event in pygame.event.get():
            self.player.handle_event(event)

        self.player.move()

    def update_monsters(self):
        for monster in self.monsters:
            monster.move()

    def draw(self):
        self.display.clear()
        for monster in self.monsters:
            monster.draw()
        self.player.draw()


def run():
    game = Game()
    try:
        game.main()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    run()
