from typing import List

from pygame.event import Event
from pygame.math import Vector2

from pharcobial.types import KeyBinding


class Controller:
    """
    Class wrapping the controller keys around and handling the
    direction and focus of the controller.
    """

    def __init__(self, bindings: KeyBinding) -> None:
        self.direction = Vector2()
        self.forward_vector = Vector2()
        self.keys_held: List[int] = []
        self.bindings = bindings
        self.activate = False

    def handle_key_down(self, event: Event):
        if event.key not in self.keys_held:
            self.keys_held.append(event.key)

        if event.key == self.bindings.left:
            self.direction.x = max(-1, self.direction.x - 1)
            self.forward_vector.x = -1

        elif event.key == self.bindings.right:
            self.direction.x = min(1, self.direction.x + 1)
            self.forward_vector.x = 1

        elif event.key == self.bindings.up:
            self.direction.y = max(-1, self.direction.y - 1)
            if self.bindings.right not in self.keys_held:
                # Characters face left when going up.
                self.forward_vector.x = -1

        elif event.key == self.bindings.down:
            self.direction.y = min(1, self.direction.y + 1)
            if self.bindings.left not in self.keys_held:
                # Characters face right when going down.
                self.forward_vector.x = 1

        elif event.key == self.bindings.activate:
            self.activate = True

        if self.direction.magnitude() not in (0, 1):
            self.direction = self.direction.normalize()

    def handle_key_up(self, event: Event):
        self.keys_held = [k for k in self.keys_held if k != event.key]

        if event.key == self.bindings.left:
            val = 1 if self.direction.x == 0 else abs(self.direction.x)
            self.direction.x = min(1, self.direction.x + val)
            self.direction.y = round(self.direction.y)
            self.forward_vector.x = 1 if self.direction.x > 0 else self.forward_vector.x

        elif event.key == self.bindings.right:
            val = 1 if self.direction.x == 0 else abs(self.direction.x)
            self.direction.x = max(-1, self.direction.x - val)
            self.direction.y = round(self.direction.y)
            self.forward_vector.x = -1 if self.direction.x < 0 else self.forward_vector.x

        elif event.key == self.bindings.down:
            val = 1 if self.direction.y == 0 else abs(self.direction.y)
            self.direction.y = max(-1, self.direction.y - val)
            self.direction.x = round(self.direction.x)
            self.forward_vector.x = -1 if self.direction.y < 0 else self.forward_vector.x

        elif event.key == self.bindings.up:
            val = 1 if self.direction.y == 0 else abs(self.direction.y)
            self.direction.y = min(1, self.direction.y + val)
            self.direction.x = round(self.direction.x)
            self.forward_vector.x = 1 if self.direction.y > 0 else self.forward_vector.x

        elif event.key == self.bindings.activate:
            self.activate = False
