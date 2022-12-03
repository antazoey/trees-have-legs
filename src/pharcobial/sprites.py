import random
from enum import Enum

import pygame
from pygame.sprite import Sprite

from pharcobial.utils import GameDisplay


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Player(Sprite):
    """
    The main character.
    """

    def __init__(self, display: GameDisplay, character: str = "pharma"):
        self.display = display
        self.character = character

        # Put in middle of screen
        self.x = display.width / 2
        self.y = display.height / 2

        self.facing = Direction.LEFT
        self.moving = False

        super().__init__()

    def draw(self):
        suffix = (
            Direction.LEFT.value
            if self.facing in (Direction.LEFT, Direction.UP)
            else Direction.RIGHT.value
        )
        image_id = f"{self.character}-{suffix}"
        self.display.show_image(image_id, self.x, self.y)

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """

        if event.type == pygame.KEYDOWN:
            # Start moving
            key_map = {
                pygame.K_LEFT: Direction.LEFT,
                pygame.K_RIGHT: Direction.RIGHT,
                pygame.K_UP: Direction.UP,
                pygame.K_DOWN: Direction.DOWN,
            }
            self.facing = key_map.get(event.key) or self.facing
            self._handle_environment()

        elif event.type == pygame.KEYUP:
            # Stop moving
            self.moving = event.key not in (
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_DOWN,
            )
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
            self.moving = new_coordinate >= self.display.block_size
        elif self.facing == Direction.RIGHT:
            self.moving = new_coordinate <= self.display.width - self.display.block_size * 4
        elif self.facing == Direction.DOWN:
            self.moving = new_coordinate <= self.display.height - self.display.block_size * 4

        return self.moving

    def move(self):
        if not self.moving or not self._handle_environment():
            return

        if self.facing == Direction.LEFT:
            self.x -= self.display.block_size
        elif self.facing == Direction.RIGHT:
            self.x += self.display.block_size
        elif self.facing == Direction.UP:
            self.y -= self.display.block_size
        elif self.facing == Direction.DOWN:
            self.y += self.display.block_size

    def eat(self, edible: "Edible"):
        threshold = 20
        x_range = range(edible.x - threshold, edible.x + threshold)
        y_range = range(edible.y - threshold, edible.y + threshold)
        if self.x in x_range and self.y in y_range:
            edible.digest()


class Edible:
    def __init__(self, display: GameDisplay):
        self.display = display
        self.x = random.randrange(20, display.width - display.block_size - 10, 10)
        self.y = random.randrange(20, display.height - display.block_size - 10, 10)
        self.show_text_iterations_remaining = 0
        self.text_timer_amount = 20

    def draw(self):
        edible = [self.x, self.y, self.display.block_size, self.display.block_size]
        self.display.draw("red", edible)
        if self.show_text_iterations_remaining > 0:
            self.display.show_text(
                "You've eaten an edible!",
                "black",
                self.display.width / 10,
                self.display.height / 10,
            )
            self.show_text_iterations_remaining -= 1

    def move(self):
        self.x = random.randrange(20, self.display.width - self.display.block_size - 10, 10)
        self.y = random.randrange(20, self.display.height - self.display.block_size - 10, 10)
        self.draw()

    def digest(self):
        self.move()
        self.show_text_iterations_remaining = self.text_timer_amount
