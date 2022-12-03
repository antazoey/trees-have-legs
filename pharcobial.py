import os
import random
from functools import cached_property
from typing import Dict, Tuple

import pygame
from pygame.sprite import Sprite

Color = Tuple[int, int, int]
RGB: Dict[str, Color] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 155, 0),
}
NAME = str(__file__).split(os.path.sep)[0].replace(".py", "").capitalize()


class GameDisplay:
    def __init__(self, width: int, height: int, block_size: int) -> None:
        self.width = width
        self.height = height
        self.block_size = block_size
        self.display = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(None, 25)
        pygame.display.set_caption(NAME)

    def message_to_screen(self, msg: str, color: Tuple[int, int, int], x, y):
        screen_text = self.font.render(msg, True, color)
        self.display.blit(screen_text, [x, y])

    def clear(self):
        self.display.fill(RGB["white"])

    def draw(self, color: str, sprite: Sprite):
        pygame.draw.rect(self.display, RGB[color], sprite)


class Clock:
    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self.fps = fps
    
    def tick(self):
        self._clock.tick(self.fps)


class Pharma(Sprite):
    def __init__(self, display: GameDisplay):
        self.display = display

        # Put in middle of screen
        self.lead_x = display.width / 2
        self.lead_y = display.height / 2
        self.head = [self.lead_x, self.lead_y]

        self.delta_x = 0
        self.delta_y = 0

        super().__init__()

    def draw(self):
        pharma = [self.lead_x, self.lead_y, self.display.block_size, self.display.block_size]
        self.display.draw("green", pharma)

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
        self.lead_x += self.delta_x
        self.lead_y += self.delta_y

    def eat(self, edible):
        if self.lead_x == edible.x and self.lead_y == edible.y:
            edible.move()
            edible.edible_message_to_screen()


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

    def edible_message_to_screen(self):
        self.display.message_to_screen(
            "You've eaten an edible!",
            RGB["black"],
            self.display.width / 10,
            self.display.height / 10,
        )


class App:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        block_size: int = 10,
        fps: int = 20,
        font_size: int = 25,
    ):
        pygame.init()
        self.display = GameDisplay(width, height, block_size)
        self.font = pygame.font.SysFont(None, font_size)
        self.clock = Clock(fps)
        self.game_exit = False
        self.game_over = False

    @cached_property
    def player(self):
        return Pharma(self.display)

    @cached_property
    def edible(self):
        return Edible(self.display)

    def main(self):
        while not self.game_exit:
            while self.game_over:
                self.end()

            self.display.clear()
            self.edible.draw()
            for event in pygame.event.get():
                self.player.handle_movement(event)

            self.player.move()
            self.player.draw()
            self.player.eat(self.edible)
            pygame.display.update()
            self.clock.tick()

    def end(self):
        self.display.clear()
        self.message_to_screen("Game over, prcess C to play again or Q to quit", RGB["red"])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.gameExit = True
                    self.gameOver = False
                if event.key == pygame.K_c:
                    run()


def run():
    game = App()
    game.main()
    pygame.quit()


if __name__ == "__main__":
    run()
