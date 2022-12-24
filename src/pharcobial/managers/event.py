from pygame import QUIT
from pygame.event import get as get_events

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction, InputEvent


class EventManager(BaseManager):
    def process(self) -> GameAction:
        """
        Allow an event to affect how sprites update.
        Event processing happens before sprites updating.
        """

        for event in get_events():
            # Handle exiting game
            escape_key = self.options.key_bindings.escape
            escape_key_pressed = event.type == InputEvent.KEY_DOWN and event.key == escape_key
            if escape_key_pressed:
                return GameAction.MENU

            elif event.type == QUIT:
                return GameAction.QUIT

            self.views.active.handle_event(event)

        return GameAction.CONTINUE


event_manager = EventManager()
