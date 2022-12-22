import pygame  # type: ignore
from pygame.math import Vector2  # type: ignore

from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.graphics import graphics_manager
from pharcobial.sprites.base import BaseSprite


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(self, x: int, y: int, character: str = "pharma"):
        super().__init__(x, y)
        self.character = character
        self.move_gfx_id: int = -1
        self.speed = 0.24
        self.uses_events: bool = True
        self.direction = Vector2()
        self.image = graphics_manager[self.character]
        self.image_flipped = False

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0

    def get_sprite_id(self) -> str:
        return "player"

    def get_gfx_id(self) -> str:
        if not self.moving:
            # Return a standing-still graphic of the last direction facing.
            return self.character

        self.move_gfx_id += 1
        frame_rate = round(self.speed * BLOCK_SIZE)
        if self.move_gfx_id in range(frame_rate):
            suffix = "-walk-1"
        elif self.move_gfx_id in range(frame_rate, frame_rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.move_gfx_id = -1

        return f"{self.character}{suffix}"

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """

        if event.type == pygame.KEYDOWN:
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
        gfx_id = self.get_gfx_id()
        self.image = graphics_manager.get(gfx_id, flip_vertically=self.image_flipped)

        if not self.moving:
            return

        length = BLOCK_SIZE * self.speed
        new_x = round(self.rect.x + self.direction.x * length)
        new_y = round(self.rect.y + self.direction.y * length)

        # Adjust coordinates. Note: must happen after setting image.
        self.move(new_x, new_y)
