from functools import cached_property

from pygame.event import Event

from treeshavelegs.constants import BLOCK_SIZE
from treeshavelegs.managers.base import ViewController
from treeshavelegs.sprites.base import InventorySprite
from treeshavelegs.types import Positional, UserInput, WorldStage


class FriendCardView(ViewController):
    SHOWN: bool = False

    @property
    def found(self) -> bool:
        return self.world.stage > WorldStage.FIND_FRIEND_CARD

    @property
    def card_id(self) -> int:
        if not self.found and not self.SHOWN:
            return 0

        return min(4, self.world.stage)

    def handle_event(self, event: Event):
        if event.type != UserInput.KEY_DOWN:
            return

        elif not self.found and self.SHOWN:
            self.world.next_stage()

        # Any key dismisses the friend-card.
        self.views.pop()

    def draw(self):
        card_id: int = self.card_id

        if card_id == 0:
            self.SHOWN = True

        self.display.show_graphic(
            f"friend-card-close-{card_id}",
            "center",
            self.display.width // (BLOCK_SIZE * 4),
            self.display.height // (BLOCK_SIZE * 4),
        )


class FriendCard(InventorySprite):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "friend-card",
            "friend-card",
            (self.world.group, self.collision.group),
            position=position,
            hitbox_inflation=(-25, -25),
        )

    @cached_property
    def friend_card_view(self) -> FriendCardView:
        return FriendCardView("friend-card")

    def inventory_select(self):
        self.views.push(self.friend_card_view)
