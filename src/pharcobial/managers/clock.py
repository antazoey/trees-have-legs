import pygame  # type: ignore

from .base import BaseManager


class Clock(BaseManager):
    def __init__(self):
        self._clock = pygame.time.Clock()

    def tick(self):
        self._clock.tick(self.options.fps)


clock = Clock()
