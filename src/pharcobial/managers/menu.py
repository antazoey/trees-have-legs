from functools import cached_property
from typing import Iterable, List

from pygame.event import Event

from pharcobial.managers.base import ViewController
from pharcobial.types import MenuItem, UserInput
from pharcobial.utils import quit


class MenuManager(ViewController):
    selected: int = 0

    @cached_property
    def main(self) -> List[MenuItem]:
        options = ("Continue", "Quit")
        items_dict = []

        for i, val in enumerate(options):
            if val == "Quit":
                fn = quit
            else:
                fn = self.hide

            item = MenuItem(title=val, index=i, action=fn)
            items_dict.append(item)

        return items_dict

    def draw(self):
        start_x = self.display.half_width // 2
        start_y = self.display.half_height // 2

        for item in self.main:
            if item.index == self.selected:
                font_size = 36
                color = "green"
                x_offset = -8
            else:
                font_size = 34
                color = "white"
                x_offset = 0

            y_offset = start_y + (item.index * font_size) + 10
            self.display.show_text(
                item.title, font_size, (start_x + x_offset, start_y + y_offset), color
            )

    def handle_event(self, event: Event):
        if event.type != UserInput.KEY_DOWN:
            return

        if event.key == self.options.key_bindings.escape:
            self.hide()

        elif event.key == self.options.key_bindings.down:
            self.selected = (self.selected + 1) % len(self)

        elif event.key == self.options.key_bindings.up:
            self.selected = (self.selected - 1) % len(self)

        elif event.key == self.options.key_bindings.enter:
            item = self.main[self.selected]
            item.action()

    def __len__(self) -> int:
        return len(self.main)

    def __iter__(self) -> Iterable[MenuItem]:
        yield from self.main

    def hide(self):
        self.visible = False
        self.views.pop()
        self.clock.paused = False


menu_manager = MenuManager()
