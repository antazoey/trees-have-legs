from typing import Iterable

from pygame.event import Event
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from pharcobial.controller import Controller
from pharcobial.sprites.base import Character
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.types import SpriteID, UserInput, GfxID


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
            character, self.map.player_start, character, groups, (-10, -20), hp, max_hp, ap
        )
        self.max_speed = speed
        self.controller = Controller(self.options.key_bindings)
        self.direction = self.controller.direction
        self.forward = self.controller.forward
        self.chat_bubble = ChatBubble(self)

    def activate(self):
        """
        The user hitting the action key on something.
        """

    def handle_event(self, event: Event):
        if event.type == UserInput.KEY_DOWN and event.key == self.controller.bindings.activate:
            self.chat_bubble.visible = True

    def update(self, *args, **kwargs):
        self.controller.update()
        self.direction = self.controller.direction
        self.forward = self.controller.forward
        self.image = self.get_graphic() or self.image

        if self.stopped:
            self.ease.reset()
            return

        elif self.coming_to_stop:
            new_x = self.hitbox.x + self.controller.forward.x * self.speed * self.ease.effect
            new_y = self.hitbox.y + self.controller.forward.y * self.speed * self.ease.effect

            if self.ease.effect > self.ease.start:
                self.ease.out()

        else:
            new_x = self.hitbox.x + self.controller.direction.x * self.speed * self.ease.effect
            new_y = self.hitbox.y + self.controller.direction.y * self.speed * self.ease.effect
            if self.ease.effect < 1:
                self.ease._in()

        self.move((new_x, new_y))

        flip = self.controller.forward.x > 0
        image = self.graphics.get(Graphics.CHAT_BUBBLE, flip_vertically=flip)
        self.chat_bubble.image = image or self.chat_bubble.image

    def die(self):
        super().die()
        self.world.you_died.visible = True
        self.hp = self.max_hp
        self.move(self.map.player_start)
