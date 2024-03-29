from treeshavelegs.sprites.base import BaseSprite, InGameItem
from treeshavelegs.types import Positional, WorldStage


class Fire(InGameItem):
    def __init__(self, position: Positional, *args, **kwargs) -> None:
        super().__init__(
            "fire",
            "fire-1",
            (self.world.group, self.collision.group),
            position=position,
            hitbox_inflation=(-10, 0),
        )
        self.gfx_index = 0
        self.gfx_total = 3
        self.gfx_delay = 5
        self.gfx_delay_index = 0

    def update(self):
        if (
            self.world.stage == WorldStage.GET_TAYLOR_BACK
            and self.is_accessible(self.sprites.runner, scalar=1.5)
            and self.sprites.runner.hysteria <= 0
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

    def handle_activate(self, activator: BaseSprite) -> bool:
        super().handle_activate(activator)

        # Allow to activate others near the fire as well.
        return False
