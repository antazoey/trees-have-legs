import re

import pygame  # type: ignore

from pharcobial._types import Direction, DrawInfo
from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.base import BaseSprite

IMAGE_ID_PATTERN = re.compile(r"(pharma-(left|right))(-walk(-\d)?)?")


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(self, character: str = "pharma"):
        super().__init__()
        self.character = character
        self.move_image_id: int = -1
        self.speed = 0.24
        self.movement_x = 0
        self.movement_y = 0
        self.active_image_id: str | None = None
        self.uses_events: bool = True

        self.keys_down = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

    @property
    def moving(self) -> bool:
        return any(x for x in self.keys_down.values())

    def get_sprite_id(self) -> str:
        return "player"

    def get_draw_info(self) -> DrawInfo:
        return DrawInfo(image_id=self._get_image_id(), coordinates=self.coordinates)

    def _get_image_id(self) -> str:
        if not self.moving and self.active_image_id is not None:
            # Return a standing-still image of the last direction facing.
            match = re.match(IMAGE_ID_PATTERN, self.active_image_id)
            assert match  # For mypy
            return match.groups()[0]

        # NOTE: Always handle LEFT / RIGHT before UP / DOWN
        # to prevent walking backwards for combos like UP + RIGHT
        if self.keys_down[Direction.LEFT]:
            suffix = Direction.LEFT.value
        elif self.keys_down[Direction.RIGHT]:
            suffix = Direction.RIGHT.value
        elif self.keys_down[Direction.UP]:
            suffix = Direction.LEFT.value
        elif self.keys_down[Direction.DOWN]:
            suffix = Direction.RIGHT.value
        elif self.active_image_id is not None:
            # Use the previous image ID if it exists
            return self.active_image_id
        else:
            suffix = Direction.LEFT.value

        self.move_image_id += 1
        frame_rate = round(self.speed * BLOCK_SIZE)
        if self.move_image_id in range(frame_rate):
            suffix = f"{suffix}-walk-1"
        elif self.move_image_id in range(frame_rate, frame_rate * 2 + 1):
            suffix = f"{suffix}-walk-2"
        else:
            self.move_image_id = -1

        self.active_image_id = f"{self.character}-{suffix}"
        return self.active_image_id

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """
        key_map = {
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
        }
        if event.type == pygame.KEYDOWN and event.key in key_map:
            # Start moving
            self.keys_down[key_map[event.key]] = True

        elif event.type == pygame.KEYUP and event.key in key_map:
            # Stop moving
            self.keys_down[key_map[event.key]] = False

    def update(self):
        if not self.moving:
            return

        movement_length = BLOCK_SIZE * self.speed

        # Update potential movement
        if self.keys_down[Direction.LEFT]:
            self.movement_x -= 1
        if self.keys_down[Direction.RIGHT]:
            self.movement_x += 1
        if self.keys_down[Direction.UP]:
            self.movement_y -= 1
        if self.keys_down[Direction.DOWN]:
            self.movement_y += 1

        if self.coordinates:
            self.previous_coordinates = self.coordinates

        self.x += round(self.movement_x * movement_length)
        self.y += round(self.movement_y * movement_length)

        # Reset movement.
        self.movement_x = 0
        self.movement_y = 0
