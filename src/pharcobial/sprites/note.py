from pygame.event import Event

from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.base import ViewController
from pharcobial.sprites.base import InventorySprite
from pharcobial.types import Positional, UserInput


class NoteView(ViewController):
    def handle_event(self, event: Event):
        if event.type != UserInput.KEY_DOWN:
            return

        self.views.pop()

    def draw(self):
        self.display.show_graphic(
            "note-close",
            (0, 0),
            self.display.width // BLOCK_SIZE,
            self.display.height // BLOCK_SIZE,
        )


class Note(InventorySprite):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "note",
            position,
            "note",
            (self.world.group, self.collision.group),
            (-25, -25),
        )

    def activate(self):
        self.views.push(NoteView("note-upclose", None))
