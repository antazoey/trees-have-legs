from pygame.event import Event

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from pharcobial.controller import Controller
from pharcobial.sprites.base import Character
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.types import SpriteID, UserInput


class GrabAnimation:
    def __init__(self) -> None:
        self.on = False
        self.time = 10  # frames
        self.time_index = 0

    def update(self):
        if not self.on:
            return

        self.time_index += 1
        if self.time_index == self.time:
            self.on = False
            self.time_index = 0


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
            (-18, -10),
            hp,
            max_hp,
            ap,
        )
        self.max_speed = speed
        self.controller = Controller(self.options.key_bindings)
        self.direction = self.controller.direction
        self.forward = self.controller.forward
        self.chat_bubble = ChatBubble(self)
        self.grab_animation = GrabAnimation()

    @property
    def is_dead(self) -> bool:
        return self.world.end_screen.visible

    def activate(self):
        """
        The user hitting the action key on something.
        """
        if self.is_accessible(self.sprites["note"], scalar=3):
            self.grab_animation.on = True

        else:
            self.chat_bubble.visible = True
            self.audio.play_sound("vocal")

    def handle_event(self, event: Event):
        if event.type == UserInput.KEY_DOWN and event.key == self.controller.bindings.activate:
            self.activate()

    def update(self, *args, **kwargs):
        if self.grab_animation.on:
            image = self.graphics.get(f"{self.gfx_id}-grab", flip_x=self.forward.x > 0)
            self.image = image or self.image
            self.grab_animation.update()
            return

        self.controller.update()
        self.direction = self.controller.direction
        self.forward = self.controller.forward
        self.gfx_id = (
            f"{Graphics.JULES}-damaged" if self.hp < 0.25 * self.max_hp else Graphics.JULES
        )
        self.walk_animation.prefix = self.gfx_id
        self.walk()
        self.chat_bubble.set_graphic(self.forward.x > 0)
        self.damage_blinker.update()

    def die(self):
        super().die()
        self.world.end_screen.lose()
        self.hp = self.max_hp
        self.sprites.reset()

    def heal(self):
        if self.hp < self.max_hp:
            self.hp += 1
