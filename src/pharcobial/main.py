from typing import List

import pygame  # type: ignore

from pharcobial.basesprite import BaseSprite
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
        self.running = False
        self.player = Player(self.display)

        # Register all initial sprites here
        self.registered_sprites: List[BaseSprite] = [
            Player(self.display),
            *[Monster(self.display, i) for i in range(options.num_monsters)],
        ]

    def run(self):
        self.display.clear()
        self.running = True
        while self.running:
            self.handle_events()
            if not self.running:
                # Exit early if event triggered end-of-game
                break

            self.update_sprites()
            self.draw_sprites()
            pygame.display.update()
            self.clock.tick()

        pygame.quit()

    def handle_events(self):
        for sprite in [e for e in self.registered_sprites if e.uses_events]:
            for event in pygame.event.get():

                # Handle game-level events
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                sprite.handle_event(event)

    def update_sprites(self):
        for sprite in self.registered_sprites:
            sprite.update()

    def draw_sprites(self):
        self.display.clear()
        for sprite in self.registered_sprites:
            sprite.draw()


def main():
    try:
        options = get_game_options()
        game = Game(options)
        game.run()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__":
    main()
