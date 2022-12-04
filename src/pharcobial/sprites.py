import random

import pygame

from pharcobial.display import GameDisplay
from pharcobial.models import BaseSprite, Coordinates, Direction


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(self, display: GameDisplay, character: str = "pharma"):
        self.display = display
        self.character = character

        # Put in middle of screen
        self.x = display.width // 2
        self.y = display.height // 2
        self.previous_coordinates: Coordinates | None = None

        self.facing = Direction.LEFT
        self.moving = False
        self.move_image_id: int = 0

        super().__init__()

    def draw(self):
        if self.previous_coordinates:
            size = self.display.block_size * 2
            self.display.draw_rect("white", self.previous_coordinates, width=size, height=size)

        image_id = self._get_image_id()
        self.display.draw_image(image_id, self.coordinates)

    def _get_image_id(self) -> str:
        suffix = (
            Direction.LEFT.value
            if self.facing in (Direction.LEFT, Direction.UP)
            else Direction.RIGHT.value
        )

        if self.moving and self.move_image_id != 1:
            self.move_image_id = 1
            suffix = f"{suffix}-walk-{self.move_image_id}"
        elif self.moving:
            self.move_image_id = 2
            suffix = f"{suffix}-walk-{self.move_image_id}"
        else:
            self.move_image_id = 0

        return f"{self.character}-{suffix}"

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
            self.facing = key_map[event.key]
            self._handle_environment()

        elif event.type == pygame.KEYUP:
            # Stop moving
            self.moving = event.key not in list(key_map.keys())
            self.moving = False

    def _handle_environment(self) -> bool:
        # Check if hitting a boundary
        coordinate = self.x if self.facing in (Direction.LEFT, Direction.RIGHT) else self.y
        amount = (
            self.display.block_size
            if self.facing in (Direction.RIGHT, Direction.DOWN)
            else -self.display.block_size
        )
        new_coordinate = coordinate + amount

        if self.facing in (Direction.LEFT, Direction.UP):
            self.moving = new_coordinate >= 0
        elif self.facing == Direction.RIGHT:
            self.moving = new_coordinate <= self.display.width - self.display.block_size * 2
        elif self.facing == Direction.DOWN:
            self.moving = new_coordinate <= self.display.height - self.display.block_size * 2

        return self.moving

    def move(self):
        if not self.moving or not self._handle_environment():
            return

        if self.coordinates:
            self.previous_coordinates = self.coordinates

        if self.facing == Direction.LEFT:
            self.x -= self.display.block_size
        elif self.facing == Direction.RIGHT:
            self.x += self.display.block_size
        elif self.facing == Direction.UP:
            self.y -= self.display.block_size
        elif self.facing == Direction.DOWN:
            self.y += self.display.block_size


class RandomlyAppearing(BaseSprite):
    def __init__(self, display: GameDisplay):
        self.display = display
        self.x = random.randrange(20, display.width - display.block_size - 10, 10)
        self.y = random.randrange(20, display.height - display.block_size - 10, 10)


class Monster(RandomlyAppearing):
    def draw(self):
        self.display.draw_image("bush-monster", self.coordinates)
