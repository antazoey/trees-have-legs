from contextlib import contextmanager
from typing import Dict

import pygame  # type: ignore
from pygame.rect import Rect  # type: ignore
from pygame.surface import Surface  # type: ignore

from pharcobial._types import Color, DrawInfo
from pharcobial.constants import NAME

from .base import BaseManager


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

    def draw_surface(self, surface: Surface, rect: Rect | None = None):
        rect = rect or Rect(0, 0, self.width, self.height)
        self.screen.blit(surface, rect)
        pygame.display.flip()

    def clear(self):
        self.screen.fill(self.RGB["white"])


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

    def draw_sprite(self, draw_info: DrawInfo):
        image = self.graphics.get(draw_info.gfx_id, orientation=draw_info.orientation)
        return self.active.draw_surface(image, rect=draw_info.rect)


display_manager = DisplayManager()
