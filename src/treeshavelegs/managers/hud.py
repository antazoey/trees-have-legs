import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from treeshavelegs.constants import BLOCK_SIZE, RGB, Graphics
from treeshavelegs.managers.base import BaseManager, ManagerAccess
from treeshavelegs.types import Positional, WorldStage


class HUDItem(ManagerAccess):
    def __init__(self, display_surface: Surface) -> None:
        self.display_surface = display_surface


class Bar(HUDItem):
    def __init__(
        self,
        surface: Surface,
        position: Positional,
        height: int,
        width: int,
        color: str,
        start: int,
        max: int,
        horizontal: bool = True,
    ) -> None:
        super().__init__(surface)
        self.height = height
        self.width = width
        self.color = color
        self.rect = Rect(*position, self.width, self.height)  # type: ignore
        self.current = start
        self.max = max
        self.horizontal = horizontal

    def draw(self):
        # Draw background
        pygame.draw.rect(self.display_surface, RGB["onyx"], self.rect)

        # Convert stat to pixels
        ratio = self.current / self.max
        filled_rect = self.rect.copy()
        if self.horizontal:
            filled_rect.width = round(self.rect.width * ratio)
        else:
            height = round(self.rect.height * ratio)
            offset = self.rect.height - height
            filled_rect.y += offset
            filled_rect.height = height

        # Draw filled-in health.
        pygame.draw.rect(self.display_surface, RGB[self.color], filled_rect)

        # Draw full health-bar border.
        pygame.draw.rect(self.display_surface, RGB["black"], self.rect, 3)


class HealthBar(Bar):
    def __init__(self) -> None:
        super().__init__(
            self.display.active.screen,
            (10, 10),
            20,
            128,
            "red",
            self.sprites.player.hp,
            self.sprites.player.max_hp,
        )

    def update(self):
        player = self.sprites.player
        self.current = player.hp
        self.max = player.max_hp


class TaylorCalmBar(Bar):
    def __init__(self) -> None:
        super().__init__(
            self.display.active.screen,
            (self.display.active.screen.get_width() - 2 * BLOCK_SIZE, 10),
            128,
            20,
            "blue",
            int(self.sprites.taylor.hysteria),
            int(self.sprites.taylor.max_hysteria),
            horizontal=False,
        )

    def update(self):
        self.current = self.sprites.taylor.hysteria

    def draw(self):
        super().draw()

        # Draw Taylor indicator.
        position = (self.rect.x - 5, self.rect.y + 90)
        self.display.show_graphic(Graphics.TAYLOR, position)


class InventoryDisplay(HUDItem):
    def __init__(self) -> None:
        super().__init__(self.display.active.screen)
        self.inventory = self.sprites.player.inventory

    def update(self):
        self.inventory = self.sprites.player.inventory

    def draw(self):
        for index, item in self.inventory.items():
            x_offset = BLOCK_SIZE + (1.5 * BLOCK_SIZE * index)
            position = (x_offset, self.display_surface.get_height() - BLOCK_SIZE * 1.2)
            self.display.show_text(
                f"{index + 1}", 8, (position[0] + 6, position[1] + 4), "white", antialias=False
            )
            self.display.show_graphic(item.gfx_id, position)
            rect = Rect(*position, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.display_surface, RGB["white"], rect, 3)


class HUDManager(BaseManager):
    """
    The organizer of the heads-up display
    (a.k.a. the health and inventory items that show on the screen).
    """

    def __init__(self) -> None:
        super().__init__()

        # Universal items.
        self.health_bar = HealthBar()
        self.inventory = InventoryDisplay()

        # Part of WorldStage.GET_TAYLOR_BACK
        self.taylor_hysteria_bar: TaylorCalmBar | None = None

    def update(self):
        self.health_bar.update()
        self.inventory.update()

        if self.world.stage == WorldStage.GET_TAYLOR_BACK:
            if self.taylor_hysteria_bar is None:
                self.taylor_hysteria_bar = TaylorCalmBar()

            self.taylor_hysteria_bar.update()

    def draw(self):
        self.health_bar.draw()
        self.inventory.draw()

        if self.world.stage == WorldStage.GET_TAYLOR_BACK:
            assert self.taylor_hysteria_bar is not None
            self.taylor_hysteria_bar.draw()


hud_manager = HUDManager()
