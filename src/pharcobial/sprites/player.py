from typing import Iterable

import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.logging import game_logger
from pharcobial.sprites.base import MobileSprite
from pharcobial.types import Position


class Controller:
    """
    Class wrapping the controller keys around and handling the
    direction and focus of the controller.
    """

    def __init__(self) -> None:
        self.direction = Vector2()
        self.right_focused: bool = False

    @property
    def x(self):
        return self.direction.x

    @property
    def y(self):
        return self.direction.y

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0

    def handle_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self.direction.x -= 1
            self.right_focused = False
        elif event.key == pygame.K_RIGHT:
            self.direction.x += 1
            self.right_focused = True
        elif event.key == pygame.K_UP:
            self.direction.y -= 1

            if self.direction.x <= 0:
                self.right_focused = False

        elif event.key == pygame.K_DOWN:
            self.direction.y += 1

            if self.direction.x >= 0:
                self.right_focused = True

    def handle_key_up(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.direction.x = 0
        elif event.key in (pygame.K_UP, pygame.K_DOWN):
            self.direction.y = 0


class Player(MobileSprite):
    """
    The main character.
    """

    def __init__(self, position: Position, groups: Iterable[Group], character: str = "pharma"):
        super().__init__(position, character, groups, Position(0, -26))
        self.move_gfx_id: int = -1
        self.speed = 2
        self.character = character
        self.controller = Controller()

    @property
    def moving(self) -> bool:
        return self.controller.moving

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
            self.controller.handle_key_down(event)

        elif event.type == pygame.KEYUP:
            self.controller.handle_key_up(event)

    def update(self, *args, **kwargs):
        self.image = self._get_graphic() or self.image

        if not self.moving:
            return

        new_x = round(self.hitbox.x + self.controller.x * self.speed)
        new_y = round(self.hitbox.y + self.controller.y * self.speed)
        position = Position(new_x, new_y)
        self.move(position)

    def _get_graphic(self) -> Surface | None:
        if not self.moving:
            # Return a standing-still graphic of the last direction facing.
            flip = self.controller.right_focused
            image = self.graphics.get(self.character, flip_vertically=flip)
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
        graphic = self.graphics.get(gfx_id, flip_vertically=self.controller.right_focused)
        return graphic or self.image
