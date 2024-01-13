from pygame import Surface
from pygame.event import Event

from treeshavelegs.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, Graphics
from treeshavelegs.controller import Controller
from treeshavelegs.sprites.base import Character, InventorySprite
from treeshavelegs.sprites.bubble import ChatBubble
from treeshavelegs.types import GfxID, SpriteID, UserInput


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
        # mypy being dumb
        self.hp: int
        self.gfx_id: GfxID
        self.image: Surface

        super().__init__(
            character,
            character,
            (self.world.group, self.collision.group),
            position=self.map.player_start,
            hitbox_inflation=(-18, -18),
            hp=hp,
            max_hp=max_hp,
            ap=ap,
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

        for item in self.sprites.in_game_items:
            if self.is_accessible(item, scalar=3):
                self.grab_animation.on = True
                item.handle_activate(self)
                return

        # Not near anything.
        self.chat_bubble.visible = True
        self.audio.play_sound("vocal")

    def handle_event(self, event: Event):
        if event.type == UserInput.KEY_DOWN and event.key == self.controller.bindings.activate:
            self.activate()

        elif event.type == UserInput.KEY_DOWN and event.key in self.controller.bindings.inventory:
            index = self.controller.bindings.number_key_to_int(event.key)
            item = self.inventory.get(index)
            if item:
                inv_sprite = self.sprites[item.gfx_id]
                assert isinstance(inv_sprite, InventorySprite)
                inv_sprite.inventory_select()

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

    def acquire(self, name: str, gfx_id: GfxID):
        self.grab_animation.on = True
        super().acquire(name, gfx_id)
