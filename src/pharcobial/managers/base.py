from functools import cached_property
from importlib import import_module
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .clock import ClockManager
    from .display import DisplayManager
    from .event import EventManager
    from .map import MapManager
    from .options import OptionsManager
    from .sprite import SpriteManager


class BaseManager:
    """
    A way to do dependency injection between all the managers.
    """

    def __init__(self) -> None:
        self.root_module = ".".join(BaseManager.__module__.split(".")[:-1])

    @cached_property
    def clock(self) -> "ClockManager":
        return cast("ClockManager", self.get_manager("clock"))

    @cached_property
    def display(self) -> "DisplayManager":
        return cast("DisplayManager", self.get_manager("display"))

    @cached_property
    def events(self) -> "EventManager":
        return cast("EventManager", self.get_manager("event"))

    @cached_property
    def map(self) -> "MapManager":
        return cast("MapManager", self.get_manager("map"))

    @cached_property
    def options(self) -> "OptionsManager":
        return cast("OptionsManager", self.get_manager("options"))

    @cached_property
    def sprites(self) -> "SpriteManager":
        return cast("SpriteManager", self.get_manager("sprite"))

    def get_manager(self, name: str) -> "BaseManager":
        module = import_module(f"{self.root_module}.{name}")
        return getattr(module, f"{name}_manager")
