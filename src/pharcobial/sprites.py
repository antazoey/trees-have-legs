import random

import pygame
from pygame.sprite import Sprite

from pharcobial.utils import GameDisplay


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

        self.delta_x = 0
        self.delta_y = 0

        super().__init__()

    def draw(self):
        self.display.show_image(self.character, self.x, self.y)

    def handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.delta_x = -self.display.block_size
                self.delta_y = 0
            elif event.key == pygame.K_RIGHT:
                self.delta_x = self.display.block_size
                self.delta_y = 0
            elif event.key == pygame.K_UP:
                self.delta_y = -self.display.block_size
                self.delta_x = 0
            elif event.key == pygame.K_DOWN:
                self.delta_y = self.display.block_size
                self.delta_x = 0

        # Stops moving when KEYUP
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.delta_x = 0
                self.delta_y = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.delta_x = 0
                self.delta_y = 0

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y

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

    def draw(self):
        edible = [self.x, self.y, self.display.block_size, self.display.block_size]
        self.display.draw("red", edible)

    def move(self):
        self.x = random.randrange(20, self.display.width - self.display.block_size - 10, 10)
        self.y = random.randrange(20, self.display.height - self.display.block_size - 10, 10)
        self.draw()

    def digest(self):
        self.move()
        self.display.show_text(
            "You've eaten an edible!",
            "black",
            self.display.width / 10,
            self.display.height / 10,
        )
