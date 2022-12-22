from contextlib import contextmanager
from typing import Dict

import pygame

from pharcobial.constants import NAME
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import Color


class Display:
    """
    A class used for displaying text or graphics on the actual screen.
    """

    RGB: Dict[str, Color] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 155, 0),
    }

    def __init__(
        self,
        width: int,
        height: int,
        font_size: int,
        full_screen: bool = False,
    ) -> None:

        modes = pygame.DOUBLEBUF
        if full_screen:
            modes |= pygame.FULLSCREEN

        # The root is the root window and should not have anything rendered to it
        # besides self.screen.
        self.window = pygame.display.set_mode((width, height), modes)

        # self.screen is scaled up to the window size to properly increase the size of all graphics.
        self.width = width // 2
        self.height = height // 2
        self.screen = pygame.Surface((self.width, self.height))

        self.font = pygame.font.SysFont("comic-sans", font_size)

        pygame.display.set_caption(NAME)

    def update(self):
        screen = pygame.transform.scale(self.screen, (self.width * 2, self.height * 2))
        self.window.blit(screen, (0, 0))
        pygame.display.update()

    def clear(self):
        self.screen.fill(self.RGB["black"])


class DisplayManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.main = Display(
            self.options.window_width,
            self.options.window_height,
            self.options.font_size,
            full_screen=self.options.full_screen,
        )
        self.active = self.main

        # Initialize in a cleared state.
        self.active.clear()

    def validate(self):
        assert self.active.window
        game_logger.debug("Display ready.")

    @property
    def width(self) -> int:
        return self.active.width

    @property
    def height(self) -> int:
        return self.active.height

    @contextmanager
    def in_same_cycle(self):
        self.active.clear()
        yield
        self.display.active.update()
        self.clock.tick()


display_manager = DisplayManager()
