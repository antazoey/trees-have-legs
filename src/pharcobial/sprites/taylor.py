from random import randint

from pharcobial.constants import Graphics
from pharcobial.logging import game_logger
from pharcobial.sprites.base import NPC
from pharcobial.types import Positional


class Taylor(NPC):
    def __init__(self, position: Positional, *args, **kwargs):
        super().__init__(
            Graphics.TAYLOR,
            position,
            Graphics.TAYLOR,
            (self.world.group, self.collision.group),
            (-20, -10),
        )
        self.start_position = position
        self.max_speed = 150
        self.focus_index = 50  # Initialize to 50 to not start off waiting still too long.
        self.attention_threshold = 96
        self.attention_threshold_range = (64, 128)
        self.max_hysteria = 100
        self.hysteria = self.max_hysteria

    def update(self, *args, **kwargs) -> None:
        if self.sprites.player.is_dead:
            self.move(self.start_position)
            self.hysteria = self.max_hysteria
            return

        elif self.hysteria <= 0:
            self.follow(self.sprites.player)

        else:
            # Is hysterical.
            if self.focus_index >= self.attention_threshold:
                self.refocus()
                self.focus_index = 0
            else:
                self.focus_index += 1

            x_before = self.rect.x
            y_before = self.rect.y
            self.forward = self.direction.copy()
            self.walk()
            if (
                self.direction.magnitude() != 0
                and self.rect.x == x_before
                and self.rect.y == y_before
            ):
                game_logger.debug("Taylor is stuck.")
                self.refocus()

    def refocus(self):
        game_logger.debug("Taylor is refocusing.")
        self.direction.x = randint(-1, 1)
        self.direction.y = randint(-1, 1)
        if not self.direction.magnitude() == 0:
            self.direction = self.direction.normalize()

        self.attention_threshold = randint(*self.attention_threshold_range)

    def activated(self):
        # The user calms Taylor.
        self.calm()

    def calm(self):
        new_value = randint(-1, 5)
        new_total = self.hysteria - new_value
        new_total = self._validate_value(new_total)
        self.hysteria = new_total

        # Slows down as gets more calm.
        self.max_speed = new_total + 50

    def get_scared(self, value: int):
        new_total = self._validate_value(self.hysteria + value)
        self.hysteria = new_total

        # Speeds up as gets more scared.
        self.max_speed = new_total + 50

    def _validate_value(self, value: int) -> int:
        if value > self.max_hysteria:
            return self.max_hysteria
        elif value < 0:
            return 0

        return value
