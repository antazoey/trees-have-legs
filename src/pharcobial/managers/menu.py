from functools import cached_property
from typing import List

from pygame.event import Event
from pyparsing import Iterator

from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.base import ViewController
from pharcobial.types import MenuItem, UserInput
from pharcobial.utils import noop, quit


class ControlsScreen(ViewController):
    def __init__(self) -> None:
        super().__init__("controls", None)
        self.last_row = -1
        self.last_column = -1

    def draw(self):
        self.draw_title("Movement Keys", 1, 1)
        for item in (
            "ARROW UP - Move up",
            "ARROW DOWN - Move down",
            "ARROW LEFT - Move left",
            "ARROW RIGHT - Move right",
        ):
            self.draw_item(item, 1, self.last_row + 1)

        self.draw_title("Action Keys", 2, 1)
        self.draw_item("SPACEBAR - activate", 2, 2)

        for i in range(1, 10):
            self.draw_item(f"{i} - Inventory item {i}", 2, self.last_row + 1)

    def draw_title(self, title: str, column: int, row: int):
        self._display(title, column, row, font_size=20)

    def draw_item(self, item: str, column: int, row: int):
        self._display(item, column, row)

    def _display(self, value: str, column: int, row: int, font_size: int = 16):
        x = BLOCK_SIZE if column == 1 else BLOCK_SIZE * column * 5
        self.display.show_text(value, font_size, (x, BLOCK_SIZE * row), "white")
        self.last_row = row
        self.last_column = column


class Menu(ViewController):
    def __init__(self, menu_id: str, choices: List[MenuItem]):
        self.choices = choices
        self.selected = 0
        super().__init__(f"{menu_id}-menu")

    def __iter__(self) -> Iterator[MenuItem]:
        yield from self.choices

    def __getitem__(self, index: int | slice) -> MenuItem | List[MenuItem]:
        return self.choices[index]

    def __len__(self) -> int:
        return len(self.choices)

    def draw(self):
        start_x = self.display.half_width // 2
        start_y = self.display.half_height // 2

        for item in self.choices:
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
            self.pop()

        elif event.key == self.options.key_bindings.down:
            self.selected = (self.selected + 1) % len(self)

        elif event.key == self.options.key_bindings.up:
            self.selected = (self.selected - 1) % len(self)

        elif event.key == self.options.key_bindings.enter:
            item = self.choices[self.selected]
            item.action()

    def pop(self):
        self.views.pop()


class OptionsMenu(Menu):
    def __init__(self):
        titles = ["Back"]
        titles.append(self._get_bool_setting("Music", not self.options.disable_music))
        titles.append(self._get_bool_setting("Sfx", not self.options.disable_sfx))

        choices: List[MenuItem] = []
        for index, title in enumerate(titles):
            if title == "Back":
                action = self.pop

            elif "Music" in title:
                action = self.change_music_setting
            elif "Sfx" in title:
                action = self.change_sfx_setting
            else:
                action = noop

            choices.append(MenuItem(title=title, index=index, action=action))

        super().__init__("options", choices)

    def change_music_setting(self):
        self.change_bool_setting("Music", "disable_music")

    def change_sfx_setting(self):
        self.change_bool_setting("Sfx", "disable_sfx")

    def change_bool_setting(self, name: str, setting_name: str):
        self.options[setting_name] = not self.options[setting_name]
        for choice in self.choices:
            if choice.title.startswith(name):
                new_title = self._get_bool_setting(name, not self.options[setting_name])
                choice.title = new_title
                break

    def _get_bool_setting(self, name: str, val: bool) -> str:
        suffix = "enabled" if val else "disabled"
        return f"{name.capitalize()} ({suffix})"


class MainMenu(Menu):
    def __init__(self):
        choices = []
        actions = {
            "Continue": self.pop,
            "Quit": quit,
            "Controls": self.go_to_controls,
            "Options": self.go_to_options_menu,
        }

        for index, title in enumerate(sorted(list(actions.keys()))):
            action = actions.get(title, self.pop)
            item = MenuItem(title=title, index=index, action=action)
            choices.append(item)

        super().__init__("main", choices)
        self.options_menu = OptionsMenu()
        self.controls_screen = ControlsScreen()

    def pop(self):
        self.views.pop()
        self.clock.paused = False

    def go_to_options_menu(self):
        self.views.push(self.options_menu)

    def go_to_controls(self):
        self.views.push(self.controls_screen)


class MenuManager(ViewController):
    @cached_property
    def main(self) -> Menu:
        return MainMenu()

    def draw(self):
        self.main.draw()

    def handle_event(self, event: Event):
        self.main.handle_event(event)


menu_manager = MenuManager("menu")
