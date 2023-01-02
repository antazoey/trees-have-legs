from pharcobial.sprites.base import InGameItem
from pharcobial.types import Positional


class Note(InGameItem):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "note",
            position,
            "note",
            (self.world.group, self.collision.group),
            (-25, -25),
        )
