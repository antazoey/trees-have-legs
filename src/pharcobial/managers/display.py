from contextlib import contextmanager

from pygame import BLEND_RGBA_MULT, DOUBLEBUF, FULLSCREEN, SRCALPHA
from pygame.display import flip, set_caption, set_mode, update
from pygame.font import Font, SysFont
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.transform import scale as scale_fn

from pharcobial.constants import GAME_NAME, RGB
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import GfxID, Positional
from pharcobial.utils.paths import game_paths


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

        modes = DOUBLEBUF
        if full_screen:
            modes |= FULLSCREEN

        # The root is the root window and should not have anything rendered to it
        # besides self.screen.
        self.window = set_mode((width, height), modes)

        # self.screen is scaled up to the window size to properly increase the size of all graphics.
        self.width = width // 2
        self.height = height // 2
        self.screen = Surface((self.width, self.height))

        self.font = SysFont("comic-sans", font_size)

        set_caption(GAME_NAME)

    def update(self):
        screen = scale_fn(self.screen, (self.width * 2, self.height * 2))
        self.window.blit(screen, (0, 0))
        update()

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
        flip()
        self.clock.tick()

    def show_graphic(
        self,
        gfx_id: GfxID,
        position: Positional | str,
        scale: int | None,
        transparent: bool = False,
    ):
        graphic = self.graphics[gfx_id]
        rect = graphic.get_rect()

        if scale:
            graphic = scale_fn(graphic, (rect.width * scale, rect.height * scale))

        if transparent:
            alpha_surface = Surface(graphic.get_size(), SRCALPHA)
            alpha_surface.fill((255, 255, 255, 90))
            graphic.blit(alpha_surface, (0, 0), special_flags=BLEND_RGBA_MULT)

        destination = self._get_destination(graphic, position)
        self.active.screen.blit(graphic, destination)

    def show_text(self, text: str, font_size: int, position: Positional | str, color: str):
        font_file = game_paths.get_font("bold_game_font_7")
        font = Font(str(font_file), font_size)
        surface = font.render(text, True, RGB[color])
        destination = self._get_destination(surface, position)
        self.active.screen.blit(surface, destination)

    def _get_destination(self, base: Surface, value: Positional | str) -> Positional | Rect:
        destination: Positional | Rect
        if value == "center":
            destination = base.get_rect(center=(self.half_width, self.half_height))
        elif not isinstance(value, str):
            destination = value
        else:
            raise TypeError(str(value))

        return destination


display_manager = DisplayManager()
