import pygame

from treeshavelegs.managers.base import BaseManager


class ClockManager(BaseManager):
    def __init__(self):
        super().__init__()
        self._clock = pygame.time.Clock()
        self.paused = False
        self.deltatime: float = 0.0

    def tick(self):
        self.deltatime = self._clock.tick(self.options.fps) / 1000


clock_manager = ClockManager()
