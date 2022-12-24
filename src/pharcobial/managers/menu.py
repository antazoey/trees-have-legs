from typing import Iterable

from pygame.event import Event

from pharcobial.managers.base import BaseManager
from pharcobial.types import InputEvent, MenuItem
from pharcobial.utils import quit


class MenuManager(BaseManager):
    OPTIONS = ("Continue", "Save", "Load", "Options", "Quit")

    selected: int = 0
    visible: bool = False

    def draw(self):
        if not self.visible:
            return

        start_x = self.display.half_width // 2
        start_y = self.display.half_height // 2

        for item in self.items:
            font_size = 33 if item.index == self.selected else 30
            offset = start_y + (item.index * font_size) + 10
            self.display.show_text(item.title, font_size, start_x, start_y + offset, "red")

    def handle_event(self, event: Event):
        if event.type != InputEvent.KEY_DOWN:
            return

        if event.key == self.options.key_bindings.escape:
            self.visible = False

        elif event.key == self.options.key_bindings.down:
            self.selected = (self.selected + 1) % len(self)

        elif event.key == self.options.key_bindings.up:
            self.selected = (self.selected - 1) % len(self)

        elif event.key == self.options.key_bindings.enter:
            match self.selected:
                case 0:  # Continue
                    self.visible = False
                    self.clock.paused = False

                case 1:  # Save
                    pass  # TODO

                case 2:  # Load
                    pass  # TODO

                case 3:  # Options
                    pass  # TODO

                case 4:  # Exit
                    quit()

    def __len__(self) -> int:
        return len(self.OPTIONS)

    def __iter__(self) -> Iterable[MenuItem]:
        yield from self.items

    @property
    def items(self) -> Iterable[MenuItem]:
        for idx, option in enumerate(self.OPTIONS):
            yield MenuItem(index=idx, title=option)

    def __next__(self, *args, **kwargs) -> MenuItem:
        return next(self.options, *args, **kwargs)

    def __getitem__(self, index: int) -> MenuItem:
        return list(self.items)[index]


menu_manager = MenuManager()
