from typing import List

from pygame.key import ScancodeWrapper  # type: ignore
from pygame.key import get_pressed
from pygame.math import Vector2

from treeshavelegs.types import KeyBinding


class Controller:
    """
    Class wrapping the controller keys around and handling the
    direction and focus of the controller.
    """

    def __init__(self, bindings: KeyBinding) -> None:
        self.direction = Vector2()
        self.forward = Vector2(x=-1, y=0)  # Init facing left.
        self.bindings = bindings

    @property
    def keys_pressed(self) -> ScancodeWrapper:
        return get_pressed()

    @property
    def movement_keys_pressed(self) -> List[int]:
        return [k for k in self.bindings.movement if self.keys_pressed[k]]

    def update(self):
        self.activate = self.keys_pressed[self.bindings.activate]

        keys = self.movement_keys_pressed
        new_direction = Vector2()
        if self.bindings.left in keys:
            new_direction.x -= 1
        if self.bindings.right in keys:
            new_direction.x += 1
        if self.bindings.up in keys:
            new_direction.y -= 1
        if self.bindings.down in keys:
            new_direction.y += 1

        if new_direction.magnitude() not in (0, 1):
            new_direction.normalize_ip()

        self.direction = new_direction

        # Always face last moving direction.
        if self.direction.magnitude() != 0:
            self.forward = self.direction.copy()
