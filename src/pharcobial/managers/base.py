from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .clock import Clock
    from .display import DisplayManager
    from .events import EventProcessor
    from .options import OptionsParser
    from .sprite import SpriteManager


class BaseManager:
    """
    A way to do dependency injection between all the managers.
    """

    @cached_property
    def clock(self) -> "Clock":
        from .clock import clock as c

        return c

    @cached_property
    def display(self) -> "DisplayManager":
        from .display import display_manager as dm

        return dm

    @cached_property
    def events(self) -> "EventProcessor":
        from .events import event_processor as ep

        return ep

    @cached_property
    def options(self) -> "OptionsParser":
        from .options import options_parser as op

        return op

    @cached_property
    def sprites(self) -> "SpriteManager":
        from .sprite import sprite_manager as sm

        return sm
