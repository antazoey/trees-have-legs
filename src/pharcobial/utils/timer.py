from pharcobial.types import Visible


class VisibilityTimer:
    def __init__(self, amount: int = 25) -> None:
        self.timer: int | None = None
        self.amount = amount  # Frames

    def update(self, target: Visible):
        if target.visible and self.timer is None:
            # Target was activated. Set a timer to show briefly.
            self.timer = self.amount

        elif target.visible and (self.timer or 0) <= 0:
            target.visible = False
            self.timer = None

        elif target.visible and self.timer is not None:
            self.timer -= 1
