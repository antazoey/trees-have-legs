from pharcobial.sprites.base import InGameItem
from pharcobial.types import Positional


class Fire(InGameItem):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "fire", position, "fire-1", (self.world.group, self.collision.group), (-10, 0)
        )
        self.gfx_index = 0
        self.gfx_total = 3
        self.gfx_delay = 5
        self.gfx_delay_index = 0

    def update(self):
        if (
            self.world.stage == 0
            and self.is_accessible(self.sprites.taylor, scalar=1.5)
            and self.sprites.taylor.hysteria <= 0
        ):
            self.world.end_screen.win()
            self.sprites.reset()
            return

        if self.is_accessible(self.sprites.player, scalar=2):
            self.sprites.player.heal()

        if self.gfx_delay_index < self.gfx_delay:
            self.gfx_delay_index += 1

        else:
            # Rotate graphic for animation purposes.
            self.gfx_index = (self.gfx_index + 1) % self.gfx_total
            self.set_image(f"fire-{self.gfx_index + 1}")
            self.gfx_delay_index = 0
