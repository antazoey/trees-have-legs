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

    @property
    def x(self):
        return self.direction.x

    @property
    def y(self):
        return self.direction.y

    def handle_key_down(self, event: Event) -> Vector2:
        if event.key not in self.keys_held:
            self.keys_held.append(event.key)

        if event.key == self.bindings.left:
            self.direction.x -= 1
            self.forward_vector.x = -1

        elif event.key == self.bindings.right:
            self.direction.x += 1
            self.forward_vector.x = 1

        elif event.key == self.bindings.up:
            self.direction.y -= 1
            if self.bindings.right not in self.keys_held:
                self.forward_vector.x = -1

        elif event.key == self.bindings.down:
            self.direction.y += 1
            if self.bindings.left not in self.keys_held:
                self.forward_vector.x = 1

        elif event.key == self.bindings.activate:
            self.activate = True

        return self.direction

    def handle_key_up(self, event: Event) -> Vector2:
        self.keys_held = [k for k in self.keys_held if k != event.key]

        if event.key == self.bindings.left:
            self.direction.x += 1
            if self.direction.x > 0:
                self.forward_vector.x = 1

        elif event.key == self.bindings.right:
            self.direction.x -= 1
            if self.direction.x < 0:
                self.forward_vector.x = -1

        elif event.key == self.bindings.down:
            self.direction.y -= 1
            if self.direction.y < 0:
                self.forward_vector.x = -1

        elif event.key == self.bindings.up:
            self.direction.y += 1
            if self.direction.y > 0:
                self.forward_vector.x = 1

        elif event.key == self.bindings.activate:
            self.activate = False

        return self.direction
