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
            (-10, -10),
        )
        self.max_speed = 150
        self.focus_index = 0
        self.attention_threshold = 96
        self.attention_threshold_range = (64, 128)

    def update(self, *args, **kwargs) -> None:
        if self.focus_index >= self.attention_threshold:
            self.refocus()
            self.focus_index = 0
        else:
            self.focus_index += 1

        x_before = self.rect.x
        y_before = self.rect.y
        self.forward = self.direction.copy()
        self.update_position()
        if self.direction.magnitude() != 0 and self.rect.x == x_before and self.rect.y == y_before:
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
        breakpoint()
