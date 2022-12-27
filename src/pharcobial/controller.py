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
        self.right_focused: bool = False
        self.keys_held: List[int] = []
        self.bindings = bindings
        self.activate = False

    @property
    def x(self):
        return self.direction.x

    @property
    def y(self):
        return self.direction.y

    @property
    def magnitude(self) -> float:
        return self.direction.magnitude()

    def handle_key_down(self, event: Event) -> Vector2:
        if event.key not in self.keys_held:
            self.keys_held.append(event.key)

        if event.key == self.bindings.left:
            self.direction.x -= abs(self.direction.x) if self.direction.x != 0.0 else 1.0
            self.right_focused = False

        elif event.key == self.bindings.right:
            self.direction.x += abs(self.direction.x) if self.direction.x != 0.0 else 1.0
            self.right_focused = True

        elif event.key == self.bindings.up:
            self.direction.y -= abs(self.direction.y) if self.direction.y != 0.0 else 1.0
            if self.bindings.right not in self.keys_held:
                self.right_focused = False

        elif event.key == self.bindings.down:
            self.direction.y += abs(self.direction.y) if self.direction.y != 0.0 else 1.0
            if self.bindings.left not in self.keys_held:
                self.right_focused = True

        elif event.key == self.bindings.activate:
            self.activate = True

        return self.normalize()

    def handle_key_up(self, event: Event) -> Vector2:
        self.keys_held = [k for k in self.keys_held if k != event.key]

        if event.key == self.bindings.left:
            self.direction.x += abs(self.direction.x) or 1

            # Also holding right key
            if self.direction.x > 0:
                self.right_focused = True

            # Also holding down
            if self.direction.y < 0:
                self.direction.y = -1

            # Also holding up
            elif self.direction.y > 0:
                self.direction.y = 1

        elif event.key == self.bindings.right:
            self.direction.x -= abs(self.direction.x) or 1

            # Also holding left
            if self.direction.x < 0:
                self.right_focused = False

            # Also holding down
            if self.direction.y < 0:
                self.direction.y = -1

            # Also holding up
            elif self.direction.y > 0:
                self.direction.y = 1

        elif event.key == self.bindings.down:
            self.direction.y -= abs(self.direction.y) or 1

            # Also holding up
            if self.direction.y < 0:
                self.right_focused = False

            # Also holding left
            if self.direction.x < 0:
                self.direction.x = -1

            # Also holding right
            elif self.direction.x > 0:
                self.direction.x = 1

        elif event.key == self.bindings.up:
            self.direction.y += abs(self.direction.y) or 1

            # Also holding down
            if self.direction.y > 0:
                self.right_focused = True

            # Also holding left
            if self.direction.x < 0:
                self.direction.x = -1

            # Also holding right
            elif self.direction.x > 0:
                self.direction.x = 1

        elif event.key == self.bindings.activate:
            self.activate = False

        return self.normalize()

    def normalize(self) -> Vector2:
        if self.magnitude > 0 and self.magnitude != 1:
            self.direction = self.direction.normalize()

        return self.direction
