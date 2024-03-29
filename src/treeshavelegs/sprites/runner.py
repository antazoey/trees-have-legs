from random import randint

from treeshavelegs.constants import BLOCK_SIZE
from treeshavelegs.logging import game_logger
from treeshavelegs.sprites.base import NPC, BaseSprite
from treeshavelegs.types import Positional, WorldStage


class Runner(NPC):
    def __init__(self, position: Positional, *args, **kwargs):
        super().__init__(
            "runner",
            self.characters.runner.gfx_id,
            (self.world.group, self.collision.group),
            position=position,
            hitbox_inflation=(-20, -15),
        )
        self.start_position = position
        self.max_speed = 150
        self.focus_index = 50  # Initialize to 50 to not start off waiting still too long.
        self.attention_threshold = 96
        self.attention_threshold_range = (64, 128)
        self.max_hysteria: int = 100
        self.hysteria: int = self.max_hysteria
        self.made_fist_move = False

    def update(self, *args, **kwargs) -> None:
        if self.world.stage < WorldStage.GET_TAYLOR_BACK:
            # Not yet in game.
            return

        elif self.world.stage > WorldStage.GET_TAYLOR_BACK:
            # Relax by fire.
            self.force_move((5 * BLOCK_SIZE, 6 * BLOCK_SIZE))
            self.set_image(self.characters.runner.gfx_id)
            return

        if self.sprites.player.is_dead:
            self.move(self.start_position)
            self.hysteria = self.max_hysteria
            return

        elif not self.made_fist_move:
            self.direction.x = 1
            self.direction.y = 1
            self.direction.normalize_ip()
            self.forward = self.direction.copy()
            self.walk()
            self.made_fist_move = True

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
            self.direction.normalize_ip()

        self.attention_threshold = randint(*self.attention_threshold_range)

    def handle_activate(self, activator: BaseSprite) -> bool:
        if (
            activator.sprite_id.endswith("-bubble")
            and self.world.stage <= WorldStage.GET_TAYLOR_BACK
        ):
            # The user calms Taylor.
            self.calm()

        elif activator == self.sprites.player and self.world.stage > WorldStage.GET_TAYLOR_BACK:
            # Switch characters.
            active_character_id = self.characters.active_character_id
            self.characters.change_character(self.characters.runner_id)
            self.characters.change_runner(active_character_id)

        return True

    def calm(self):
        new_value = randint(-2, 8)
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
