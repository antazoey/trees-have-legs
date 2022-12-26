from functools import cached_property
from importlib import import_module
from typing import TYPE_CHECKING, cast

from pygame.event import Event
from pygame.sprite import AbstractGroup

if TYPE_CHECKING:
    from .clock import ClockManager
    from .collision import CollisionManager
    from .display import DisplayManager
    from .event import EventManager
    from .graphics import GraphicsManager
    from .hud import HUDManager
    from .map import MapManager
    from .menu import MenuManager
    from .options import OptionsManager
    from .sprite import SpriteManager
    from .state import StateManager
    from .view import ViewManager
    from .world import WorldManager


class ManagerAccess:
    """
    A way to do dependency injection between all the managers.
    """

    @cached_property
    def clock(self) -> "ClockManager":
        """
        Responsible for overall game framerate.
        """

        return cast("ClockManager", self._("clock"))

    @cached_property
    def collision(self) -> "CollisionManager":
        """
        Responsible for detecting collision between sprites and managing the
        collision-sprite group.
        """

        return cast("CollisionManager", self._("collision"))

    @cached_property
    def display(self) -> "DisplayManager":
        """
        Responsible for showing things on the screen.
        """

        return cast("DisplayManager", self._("display"))

    @cached_property
    def events(self) -> "EventManager":
        """
        Responsible for handling events, such as key-down events.
        """

        return cast("EventManager", self._("event"))

    @cached_property
    def graphics(self) -> "GraphicsManager":
        """
        An easy way to access graphics.
        """

        return cast("GraphicsManager", self._("graphics"))

    @cached_property
    def hud(self) -> "HUDManager":
        """
        The inventory manger. Manages inventory for all sprites.
        """

        return cast("HUDManager", self._("hud"))

    @cached_property
    def map(self) -> "MapManager":
        """
        Responsible for loading .csv files and turning them into game maps.
        """

        return cast("MapManager", self._("map"))

    @cached_property
    def menu(self) -> "MenuManager":
        """
        Responsible for the pause menu.
        """

        return cast("MenuManager", self._("menu"))

    @cached_property
    def options(self) -> "OptionsManager":
        """
        Game options, as set from CLI or config.
        """

        return cast("OptionsManager", self._("options"))

    @cached_property
    def sprites(self) -> "SpriteManager":
        """
        Responsible for creating sprites and adding them to the proper
        sprite groups, such as ``.camera`` or ``.collision``.
        Holds references to all sprites in the game.
        """

        return cast("SpriteManager", self._("sprite"))

    @cached_property
    def state(self) -> "StateManager":
        """
        Responsible for saving and loading.
        """

        return cast("StateManager", self._("state"))

    @cached_property
    def views(self) -> "ViewManager":
        """
        The view stack for popping and pushing.
        """

        return cast("ViewManager", self._("view"))

    @cached_property
    def world(self) -> "WorldManager":
        """
        Responsible for the camera and sprite group for all in-world sprites.
        """

        return cast("WorldManager", self._("world"))

    def _(self, name: str) -> "BaseManager":
        module = import_module(f"{ROOT_MODULE}.{name}")
        return getattr(module, f"{name}_manager")


class BaseManager(ManagerAccess):
    def validate(self):
        """
        Override to raise assertions if needed.
        Used for ensuring managers are initialized in the proper order
        in ``GameManager.validate()``.
        """


class ViewController(BaseManager):
    def __init__(self, group: AbstractGroup | None = None) -> None:
        super().__init__()
        self.group = group

    def handle_event(self, event: Event):
        """
        Handle events from the user or OS.
        """

    def update(self, *args, **kwargs):
        """
        Update sprites in the sprite group.
        """
        if self.group:
            self.group.update(*args, **kwargs)

    def draw(self):
        """
        Draw sprites that are managed here.
        For example, the menu manager draws menu items and the camera manager draws
        the sprites in the camera sprite group.
        """

    def run(self):
        """Run the view."""
        self.update()
        with self.display.in_same_cycle():
            self.draw()


ROOT_MODULE = ".".join(BaseManager.__module__.split(".")[:-1])


__all__ = ["BaseManager"]
