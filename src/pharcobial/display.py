from pathlib import Path
from typing import Dict

import pygame

from pharcobial._types import Color, Coordinates
from pharcobial.constants import DEFAULT_BLOCK_SIZE, NAME


class Images:
    BASE_PATH = Path(__file__).parent.parent.parent / "gfx"

    @classmethod
    def load(cls, name: str):
        path = cls.BASE_PATH / f"{name}.png"
        return pygame.image.load(str(path))


class Beacon:
    player: Coordinates | None = None
    monsters: Dict[int, Coordinates] = {}


class GameDisplay:
    RGB: Dict[str, Color] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 155, 0),
    }

    def __init__(
        self, width: int, height: int, font_size: int, block_size: int = DEFAULT_BLOCK_SIZE
    ) -> None:
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.font = pygame.font.SysFont("comic-sans", font_size)
        self.beacon = Beacon()
        pygame.display.set_caption(NAME)

    def draw_image(self, image_id: str, coordinates: Coordinates):
        image = Images.load(image_id)
        self.screen.blit(image, coordinates)
        pygame.display.flip()

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
        width = width if width is not None else self.block_size
        height = height if height is not None else self.block_size
        data = [*coordinates, width, height]
        pygame.draw.rect(self.screen, self.RGB[color], data)

    def turn_off(self):
        self.clear()
        self.draw_text(
            "Game over, prcess C to play again or Q to quit",
            "red",
            self.width // 2,
            self.height // 2,
        )
        pygame.display.update()
