from pygame.event import Event

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from pharcobial.controller import Controller
from pharcobial.sprites.base import Character
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.types import SpriteID, UserInput


class Player(Character):
    """
    The main character.
    """

    def __init__(
        self,
        character: SpriteID = Graphics.JULES,
        speed: int = 128,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ):
        super().__init__(
            character,
            self.map.player_start,
            character,
            (self.world.group, self.collision.group),
            (-10, -10),
            hp,
            max_hp,
            ap,
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
        self.chat_bubble.visible = True

    def handle_event(self, event: Event):
        if event.type == UserInput.KEY_DOWN and event.key == self.controller.bindings.activate:
            self.activate()

    def update(self, *args, **kwargs):
        self.controller.update()
        self.direction = self.controller.direction
        self.forward = self.controller.forward
        self.update_position()
        flip = self.forward.x > 0
        image = self.graphics.get(Graphics.CHAT_BUBBLE, flip_vertically=flip)
        self.chat_bubble.image = image or self.chat_bubble.image

    def die(self):
        super().die()
        self.world.you_died.visible = True
        self.hp = self.max_hp
        self.move(self.map.player_start)
