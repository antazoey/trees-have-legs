from functools import cached_property
from typing import List

import pygame  # type: ignore

from pharcobial.collision import CollisionDetector
from pharcobial.display import GameDisplay
from pharcobial.monster import Monster
from pharcobial.options import GameOptions, get_game_options
from pharcobial.player import Player


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self.fps = fps

    def tick(self):
        self._clock.tick(self.fps)


class Game:
    def __init__(self, options: GameOptions):
        pygame.init()
        self.display = GameDisplay(options.width, options.height, options.font_size)
        self.clock = Clock(options.fps)
        self.game_exit = False
        self.num_monsters = options.num_monsters

    @cached_property
    def player(self) -> Player:
        return Player(self.display, self.collision_detector)

    @cached_property
    def monsters(self) -> List[Monster]:
        return [
            Monster(self.display, self.collision_detector, index)
            for index in range(self.num_monsters)
        ]

    @cached_property
    def collision_detector(self) -> CollisionDetector:
        return CollisionDetector(self.display)

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
    try:
        options = get_game_options()
        game = Game(options)
        game.main()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    run()
