from pathlib import Path
from typing import Dict

import pygame  # type: ignore

from pharcobial._types import Color, Coordinates, Direction, DrawInfo
from pharcobial.constants import BLOCK_SIZE, NAME

from .base import BaseManager


class Images:
    BASE_PATH = Path(__file__).parent.parent.parent.parent / "gfx"

    @classmethod
    def load(cls, name: str):
        path = cls.BASE_PATH / f"{name}.png"
        image = pygame.image.load(str(path))
        image.convert_alpha()  # Allows transparency
        return image


class Display:
    """
    A class used for displaying text or images on the actual screen.
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

        # self.screen is scaled up to the window size to properly increase the size of all images.
        self.width = width // 2
        self.height = height // 2
        self.screen = pygame.Surface((self.width, self.height))

        self.font = pygame.font.SysFont("comic-sans", font_size)
        self.image_cache: Dict = {}
        self.map_pointer = (0, 0)

        pygame.display.set_caption(NAME)

    def update(self):
        screen = pygame.transform.scale(self.screen, (self.width * 2, self.height * 2))
        self.window.blit(screen, (0, 0))
        pygame.display.update()

    def draw_image(
        self, image_id: str, coordinates: Coordinates, orientation: Direction | None = None
    ):
        image = Images.load(image_id)

        if orientation == Direction.RIGHT:
            image = pygame.transform.flip(image, True, False)

        self.screen.blit(image, coordinates)
        pygame.display.flip()

    def get(self, image_id: str, orientation: Direction | None = None):
        if orientation == Direction.RIGHT:
            # Handle the case where we need to flip the image vertically.
            image_cache_id = f"{image_id}-{Direction.RIGHT.value}"
            if image_cache_id in self.image_cache:
                return self.image_cache[image_cache_id]

            image = self.get(image_id)
            image = pygame.transform.flip(image, True, False)
            self.image_cache[image_cache_id] = image
            return image

        elif image_id in self.image_cache:
            return self.image_cache[image_id]

        image = Images.load(image_id)
        self.image_cache[image_id] = image
        return image

    def draw_text(self, msg: str, color: str, x: int, y: int):
        text = self.font.render(msg, True, self.RGB[color])
        self.screen.blit(text, [x, y])

    def clear(self):
        self.screen.fill(self.RGB["white"])

    def draw_rect(
        self,
        color: str,
        coordinates: Coordinates,
        width: int | None = None,
        height: int | None = None,
    ):
        width = width if width is not None else BLOCK_SIZE
        height = height if height is not None else BLOCK_SIZE
        data = [*coordinates, width, height]
        pygame.draw.rect(self.screen, self.RGB[color], data)


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

    def draw(self, draw_info: DrawInfo):
        return self.active.draw_image(
            draw_info.image_id, draw_info.coordinates, orientation=draw_info.orientation
        )


display_manager = DisplayManager()
