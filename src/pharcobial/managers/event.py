import pygame

from pharcobial.managers.base import BaseManager
from pharcobial.types import GameAction


class EventManager(BaseManager):
    def process_next(self) -> GameAction:
        """
        Allow an event to affect how sprites update.
        Event processing happens before sprites updating.
        """

        for event in pygame.event.get():
            # Handle exiting game
            escape_key_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            if escape_key_pressed:
                return GameAction.MENU

            elif event.type == pygame.QUIT:
                return GameAction.QUIT

            self.sprites.handle_event(event)

        return GameAction.CONTINUE


event_manager = EventManager()
