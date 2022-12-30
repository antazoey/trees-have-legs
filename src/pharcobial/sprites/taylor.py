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
        self.start_position = position
        self.max_speed = 150
        self.focus_index = 50  # Initialize to 50 to not start off waiting still too long.
        self.attention_threshold = 96
        self.attention_threshold_range = (64, 128)
        self.hysteria = 100

    def update(self, *args, **kwargs) -> None:
        if self.sprites.player.is_dead:
            self.move(self.start_position)
            self.hysteria = 100
            return

        elif self.hysteria <= 0:
            self.walk_towards(self.sprites.player.hitbox)

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
        new_value = randint(-1, 2)
        new_total = self.hysteria - new_value
        if new_total < 100:
            self.hysteria = new_total
            self.max_speed = new_total + 50
