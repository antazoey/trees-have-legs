from typing import Iterable

from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from pharcobial.controller import Controller
from pharcobial.sprites.base import Character
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.types import SpriteID


class Player(Character):
    """
    The main character.
    """

    def __init__(
        self,
        groups: Iterable[Group],
        character: SpriteID = Graphics.PHARMA,
        speed: int = 128,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ):
        super().__init__(
            character, self.map.player_start, character, groups, (0, -10), hp, max_hp, ap
        )
        self.move_gfx_id: int = -1
        self.max_speed = speed
        self.controller = Controller(self.options.key_bindings)
        self.direction = self.controller.direction
        self.chat_bubble = ChatBubble(self)

        self.ease_effect_min = 0.8
        self.ease_effect = self.ease_effect_min
        self.slide_increment = 0.002
        self.slide_start = 0.02
        self.slide = self.slide_start

    @property
    def stopped(self) -> bool:
        return not self.moving and self.ease_effect <= self.ease_effect_min

    @property
    def coming_to_stop(self) -> bool:
        return not self.moving and self.ease_effect > self.ease_effect_min

    @property
    def accelerating(self) -> bool:
        return self.moving and self.ease_effect < 1

    def activate(self):
        """
        The user hitting the action key on something.
        """

    def update(self, *args, **kwargs):
        self.controller.update()
        self.direction = self.controller.direction
        self.image = self._get_graphic() or self.image

        if self.stopped:
            self.slide = self.slide_start
            self.ease_effect = self.ease_effect_min
            return

        elif self.coming_to_stop:
            new_x = self.hitbox.x + self.controller.forward.x * self.speed * self.ease_effect
            new_y = self.hitbox.y + self.controller.forward.y * self.speed * self.ease_effect

            if self.ease_effect > self.ease_effect_min:
                self.ease_effect -= self.slide
                self.slide += self.slide_increment

        else:
            new_x = self.hitbox.x + self.controller.direction.x * self.speed * self.ease_effect
            new_y = self.hitbox.y + self.controller.direction.y * self.speed * self.ease_effect
            if self.ease_effect < 1:
                self.ease_effect += self.slide
                self.slide += self.slide_increment

        self.move((new_x, new_y))

        flip = self.controller.forward.x > 0
        image = self.graphics.get(Graphics.CHAT_BUBBLE, flip_vertically=flip)
        self.chat_bubble.image = image or self.chat_bubble.image

    def _get_graphic(self) -> Surface | None:
        if self.stopped:
            # Return a standing-still graphic of the last direction facing.
            flip = self.controller.forward.x > 0
            image = self.graphics.get(self.sprite_id, flip_vertically=flip)
            return image or self.image

        self.move_gfx_id += 1
        ease = self.ease_effect if self.accelerating else 1 / self.ease_effect
        rate = round(self.max_speed / 24 * ease)
        if self.move_gfx_id in range(rate):
            suffix = "-walk-1"
        elif self.move_gfx_id in range(rate, rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.move_gfx_id = -1

        gfx_id = f"{self.sprite_id}{suffix}"
        flip = self.controller.forward.x > 0
        graphic = self.graphics.get(gfx_id, flip_vertically=flip)
        return graphic or self.image
