from typing import List, Union

from treeshavelegs.managers.base import BaseManager, ViewController


class ViewManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.stack: List[ViewController] = []

    @property
    def active(self) -> ViewController:
        """
        The active view.
        """
        if not self.stack:
            self.push(self.world)

        return self.stack[-1]

    def __len__(self) -> int:
        _ = self.active  # Ensure we have 1.
        return len(self.stack)

    def __contains__(self, view: Union[ViewController, str]) -> bool:
        sought = view if isinstance(view, str) else view.view_id
        return any(x.view_id == sought for x in self.stack)

    def push(self, view: ViewController):
        """
        Push a view to the stack.
        """
        self.stack.append(view)

    def pop(self) -> ViewController:
        """
        Pop a view from the stack.
        """
        return self.stack.pop()

    def goto(self, view: Union[ViewController, str]):
        """
        Either pop back to a view if it is in the stack.
        Else, push the new view on the stack.
        """
        sought = view if isinstance(view, str) else view.view_id
        if view in self:
            while self.active.view_id != sought:
                self.pop()

        elif isinstance(view, ViewController):
            self.push(view)


view_manager = ViewManager()
