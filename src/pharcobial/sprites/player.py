from typing import Iterable, Tuple

import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.constants import BLOCK_SIZE
from pharcobial.logging import game_logger
from pharcobial.sprites.base import MobileSprite


class Player(MobileSprite):
    """
    The main character.
    """

    def __init__(
        self, position: Tuple[int, int], groups: Iterable[Group], character: str = "pharma"
    ):
        super().__init__(position, character, groups)
        self.move_gfx_id: int = -1
        self.speed = 2
        self.uses_events: bool = True
        self.direction = Vector2()
        self.character = character
        self.image_flipped = False

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0

    def get_sprite_id(self) -> str:
        return "player"

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """

        if event.type == pygame.KEYDOWN:
            game_logger.debug(f"{event.key} key pressed.")

            if event.key == pygame.K_LEFT:
                self.direction.x -= 1
            elif event.key == pygame.K_RIGHT:
                self.direction.x += 1
            elif event.key == pygame.K_UP:
                self.direction.y -= 1
            elif event.key == pygame.K_DOWN:
                self.direction.y += 1

            self.image_flipped = self.direction.x > 0 or (
                self.direction.y < 0 and self.direction.x >= 0
            )

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.direction.x = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                self.direction.y = 0

    def update(self, *args, **kwargs):
        self.image = self._get_graphic() or self.image

        if not self.moving:
            return

        new_x = round(self.rect.x + self.direction.x * self.speed)
        new_y = round(self.rect.y + self.direction.y * self.speed)

        # Check for collisions here.
        if new_x < 0:
            new_x = 0
        elif new_x > self.display.width * 2:
            new_x = self.display.width * 2
        if new_y < 0:
            new_y = 0

        # Adjust coordinates. Note: must happen after setting image.
        self.move(new_x, new_y)

    def _get_graphic(self) -> Surface | None:
        if not self.moving:
            # Return a standing-still graphic of the last direction facing.
            image = self.graphics.get(self.character, flip_vertically=self.image_flipped)
            return image or self.image

        self.move_gfx_id += 1
        rate = round(self.speed * 4)
        if self.move_gfx_id in range(rate):
            suffix = "-walk-1"
        elif self.move_gfx_id in range(rate, rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.move_gfx_id = -1

        gfx_id = f"{self.character}{suffix}"
        graphic = self.graphics.get(gfx_id, flip_vertically=self.image_flipped)
        return graphic or self.image
