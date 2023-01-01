from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.base import NPC
from pharcobial.types import Positional


class Fire(NPC):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "fire", position, "fire-1", (self.world.group, self.collision.group), (-10, 0)
        )
        self.gfx_index = 0
        self.gfx_total = 3
        self.gfx_delay = 5
        self.gfx_delay_index = 0

    def update(self):
        if self.is_reachable(self.sprites.taylor.rect.inflate(BLOCK_SIZE // 2, BLOCK_SIZE // 2)):
            self.world.end_screen.win()
            return

        if self.is_reachable(self.sprites.player.rect.inflate(BLOCK_SIZE, BLOCK_SIZE)):
            self.sprites.player.heal()

        if self.gfx_delay_index < self.gfx_delay:
            self.gfx_delay_index += 1

        else:
            # Rotate graphic for animation purposes.
            self.gfx_index = (self.gfx_index + 1) % self.gfx_total
            self.set_image(f"fire-{self.gfx_index + 1}")
            self.gfx_delay_index = 0
