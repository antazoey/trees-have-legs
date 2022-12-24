from typing import List

from pharcobial.managers.base import BaseManager, ViewController


class ViewManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.stack: List[ViewController] = []

    @property
    def active(self) -> ViewController:
        """
        The active view.
        """
        return self.stack[-1]

    def push(self, view_controller: ViewController):
        """
        Push a view to the stack.
        """
        self.stack.append(view_controller)

    def pop(self) -> ViewController:
        """
        Pop a view from the stack.
        """
        return self.stack.pop()


view_manager = ViewManager()
