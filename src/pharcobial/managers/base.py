from functools import cached_property
from importlib import import_module
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .camera import CameraManager
    from .clock import ClockManager
    from .collision import CollisionManager
    from .display import DisplayManager
    from .event import EventManager
    from .graphics import GraphicsManager
    from .map import MapManager
    from .options import OptionsManager
    from .sprite import SpriteManager
    from .state import StateManager


class BaseManager:
    """
    A way to do dependency injection between all the managers.
    """

    @cached_property
    def camera(self) -> "CameraManager":
        """
        Responsible for the offset from the active display to the active map
        and managing the camera sprite group.
        """

        return cast("CameraManager", self._get_manager("camera"))

    @cached_property
    def clock(self) -> "ClockManager":
        """
        Responsible for overall game framerate.
        """

        return cast("ClockManager", self._get_manager("clock"))

    @cached_property
    def collision(self) -> "CollisionManager":
        """
        Responsible for detecting collision between sprites and managing the
        collision-sprite group.
        """

        return cast("CollisionManager", self._get_manager("collision"))

    @cached_property
    def display(self) -> "DisplayManager":
        """
        Responsible for showing things on the screen.
        """

        return cast("DisplayManager", self._get_manager("display"))

    @cached_property
    def events(self) -> "EventManager":
        """
        Responsible for handling events, such as key-down events.
        """

        return cast("EventManager", self._get_manager("event"))

    @cached_property
    def graphics(self) -> "GraphicsManager":
        """
        An easy way to access graphics.
        """

        return cast("GraphicsManager", self._get_manager("graphics"))

    @cached_property
    def map(self) -> "MapManager":
        """
        Responsible for loading .csv files and turning them into game maps.
        """

        return cast("MapManager", self._get_manager("map"))

    @cached_property
    def options(self) -> "OptionsManager":
        """
        Game options, as set from CLI or config.
        """

        return cast("OptionsManager", self._get_manager("options"))

    @cached_property
    def sprites(self) -> "SpriteManager":
        """
        Responsible for creating sprites and adding them to the proper
        sprite groups, such as ``.camera`` or ``.collision``.
        Holds references to all sprites in the game.
        """

        return cast("SpriteManager", self._get_manager("sprite"))
    
    @cached_property
    def state(self) -> "StateManager":
        """
        Responsible for saving and loading.
        """

        return cast("StateManager", self._get_manager("state"))

    def validate(self):
        """
        Override to raise assertions if needed.
        Used for ensuring managers are initialized in the proper order
        in ``GameManager.validate()``.
        """

    def _get_manager(self, name: str) -> "BaseManager":
        module = import_module(f"{ROOT_MODULE}.{name}")
        return getattr(module, f"{name}_manager")


ROOT_MODULE = ".".join(BaseManager.__module__.split(".")[:-1])


__all__ = ["BaseManager"]
