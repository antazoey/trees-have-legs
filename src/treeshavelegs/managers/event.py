from typing import Iterable

from pygame import QUIT
from pygame.event import get as get_events

from treeshavelegs.constants import Views
from treeshavelegs.managers.base import BaseManager
from treeshavelegs.types import GameEvent, UserInput


class EventManager(BaseManager):
    @property
    def queue(self) -> Iterable[GameEvent]:
        """
        Allow an event to affect how sprites update.
        Event processing happens before sprites updating.
        """

        for event in get_events():
            # Handle exiting game
            escape_key = self.options.key_bindings.escape
            escape_key_pressed = event.type == UserInput.KEY_DOWN and event.key == escape_key
            if escape_key_pressed and Views.MENU not in self.views.active.view_id:
                yield GameEvent.MENU
                return  # Return early to prevent double-processing.

            elif event.type == QUIT:
                yield GameEvent.QUIT
                return  # No need to continue processing events.

            self.views.active.handle_event(event)

            # Continue before processing next event.
            yield GameEvent.CONTINUE

        else:
            # No events.
            yield GameEvent.CONTINUE


event_manager = EventManager()
