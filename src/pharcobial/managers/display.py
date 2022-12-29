from contextlib import contextmanager

import pygame

from pharcobial.constants import GAME_NAME, RGB
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.utils import game_paths
from pharcobial.types import Positional


class Display:
    """
    A class used for displaying text or graphics on the actual screen.
    """

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

        pygame.display.set_caption(GAME_NAME)

    def update(self):
        screen = pygame.transform.scale(self.screen, (self.width * 2, self.height * 2))
        self.window.blit(screen, (0, 0))
        pygame.display.update()

    def clear(self):
        self.screen.fill(RGB["black"])


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

    @property
    def half_width(self) -> int:
        return self.width // 2

    @property
    def half_height(self) -> int:
        return self.height // 2

    @contextmanager
    def in_same_cycle(self):
        self.active.clear()
        yield
        self.tick()

    def tick(self):
        self.display.active.update()
        pygame.display.flip()
        self.clock.tick()

    def show_text(self, text: str, font_size: int, position: Positional | str, color: str):
        font_file = game_paths.get_font("bold_game_font_7")
        font = pygame.font.Font(str(font_file), font_size)
        text = font.render(text, True, RGB[color])

        if position == "center":
            position = text.get_rect(center=(self.half_width, self.half_height))

        self.active.screen.blit(text, position)


display_manager = DisplayManager()
