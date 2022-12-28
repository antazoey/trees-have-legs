from typing import Iterable

from pygame.event import Event
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from pharcobial.controller import Controller
from pharcobial.logging import game_logger
from pharcobial.sprites.base import Character
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.types import UserInput


class Player(Character):
    """
    The main character.
    """

    def __init__(
        self,
        groups: Iterable[Group],
        character: str = Graphics.PHARMA,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ):
        super().__init__(
            character, self.map.player_start, character, groups, (0, -10), hp, max_hp, ap
        )
        self.move_gfx_id: int = -1
        self.speed = 2
        self.controller = Controller(self.options.key_bindings)
        self.direction = self.controller.direction
        self.chat_bubble = ChatBubble(self)

    def handle_event(self, event: Event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """

        if event.type == UserInput.KEY_DOWN:
            game_logger.debug(f"{event.key} key pressed.")
            self.controller.handle_key_down(event)
            self.direction = self.controller.direction
            self.chat_bubble.visible = self.controller.activate

        elif event.type == UserInput.KEY_UP:
            self.controller.handle_key_up(event)
            self.direction = self.controller.direction

    def activate(self):
        """
        The user hitting the action key on something.
        """

    def update(self, *args, **kwargs):
        self.image = self._get_graphic() or self.image

        if not self.moving:
            return

        new_x = round(self.hitbox.x + self.controller.x * self.speed)
        new_y = round(self.hitbox.y + self.controller.y * self.speed)
        self.move((new_x, new_y))
        flip = self.controller.forward_vector.x > 0
        image = self.graphics.get(Graphics.CHAT_BUBBLE, flip_vertically=flip)
        self.chat_bubble.image = image or self.chat_bubble.image

    def _get_graphic(self) -> Surface | None:
        if not self.moving:
            # Return a standing-still graphic of the last direction facing.
            flip = self.controller.forward_vector.x > 0
            image = self.graphics.get(self.sprite_id, flip_vertically=flip)
            return image or self.image

        self.move_gfx_id += 1
        rate = round(self.speed * 4)
        if self.move_gfx_id in range(rate):
            suffix = "-walk-1"
        elif self.move_gfx_id in range(rate, rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.move_gfx_id = -1

        gfx_id = f"{self.sprite_id}{suffix}"
        flip = self.controller.forward_vector.x > 0
        graphic = self.graphics.get(gfx_id, flip_vertically=flip)
        return graphic or self.image
