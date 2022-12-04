import random
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from pharcobial._types import Coordinates, Direction
from pharcobial.constants import DEFAULT_BLOCK_SIZE
from pharcobial.motion import MotionGranter, MotionRequest

if TYPE_CHECKING:
    from pharcobial.display import GameDisplay


class BaseSprite(Sprite):
    x: int = 0
    y: int = 0
    height: int = DEFAULT_BLOCK_SIZE
    width: int = DEFAULT_BLOCK_SIZE

    def __init__(self, display: "GameDisplay", motion_granter: MotionGranter) -> None:
        super().__init__()
        self.display = display
        self.motion_granter = motion_granter
        self.previous_coordinates: Coordinates | None = None
        self.facing = Direction.LEFT

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(self.x, self.y)

    @property
    def can_move(self) -> bool:
        request = MotionRequest(start_coordinates=self.coordinates, direction=self.facing)
        return self.motion_granter.can_move(request)

    def clear_previous_spot(self):
        if self.previous_coordinates:
            size = self.display.block_size * 2
            self.display.draw_rect("white", self.previous_coordinates, width=size, height=size)


class RandomlyAppearing(BaseSprite):
    def __init__(self, display: "GameDisplay", motion_granter: MotionGranter):
        super().__init__(display, motion_granter)
        self.x = random.randrange(20, display.width - display.block_size - 10, 10)
        self.y = random.randrange(20, display.height - display.block_size - 10, 10)
