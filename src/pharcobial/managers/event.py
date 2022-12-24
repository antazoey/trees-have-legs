from typing import Iterable

from pygame import QUIT
from pygame.event import get as get_events

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction, InputEvent


class EventManager(BaseManager):
    def __iter__(self) -> Iterable[GameAction]:
        """
        Allow an event to affect how sprites update.
        Event processing happens before sprites updating.
        """

        for event in get_events():
            # Handle exiting game
            escape_key = self.options.key_bindings.escape
            escape_key_pressed = event.type == InputEvent.KEY_DOWN and event.key == escape_key
            if escape_key_pressed:
                yield GameAction.MENU

            elif event.type == QUIT:
                yield GameAction.QUIT

            self.views.active.handle_event(event)
        
            # Continue before processing next event.
            yield GameAction.CONTINUE

        else:
            # No events.
            yield GameAction.CONTINUE


event_manager = EventManager()
