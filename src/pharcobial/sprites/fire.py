from pharcobial.sprites.base import NPC
from pharcobial.types import Positional


class Fire(NPC):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "fire", position, "fire-1", (self.world.group, self.collision.group), (0, 0)
        )
        self.gfx_index = 0
        self.gfx_total = 3
        self.gfx_delay = 5
        self.gfx_delay_index = 0
