import os
from typing import Dict, Tuple

import pygame
from pygame.sprite import Sprite

Color = Tuple[int, int, int]
NAME = str(__file__).split(os.path.sep)[0].replace(".py", "").capitalize()


class GameDisplay:
    RGB: Dict[str, Color] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 155, 0),
    }

    def __init__(self, width: int, height: int, block_size: int, font_size: int) -> None:
        self.width = width
        self.height = height
        self.block_size = block_size
        self.display = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(None, font_size)
        pygame.display.set_caption(NAME)

    def show_text(self, msg: str, color: str, x: int, y: int):

        screen_text = self.font.render(msg, True, self.RGB[color])
        self.display.blit(screen_text, [x, y])

    def clear(self):
        self.display.fill(self.RGB["white"])

    def draw(self, color: str, sprite: Sprite):
        pygame.draw.rect(self.display, self.RGB[color], sprite)

    def turn_off(self):
        self.clear()
        self.show_text(
            "Game over, prcess C to play again or Q to quit", "red", self.width / 2, self.height / 2
        )
        pygame.display.update()


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self.fps = fps

    def tick(self):
        self._clock.tick(self.fps)
