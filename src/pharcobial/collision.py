from dataclasses import dataclass
from functools import cached_property

from pharcobial._types import Coordinates, Direction
from pharcobial.constants import DEFAULT_BLOCK_SIZE
from pharcobial.display import GameDisplay


@dataclass
class MotionRequest:
    start_coordinates: Coordinates
    direction: Direction
    amount: int = DEFAULT_BLOCK_SIZE

    @cached_property
    def new_coordinates(self) -> Coordinates:
        x, y = self.start_coordinates

        if self.direction == Direction.LEFT:
            return Coordinates(x=x - self.amount, y=y)
        elif self.direction == Direction.RIGHT:
            return Coordinates(x=x + self.amount, y=y)
        elif self.direction == Direction.UP:
            return Coordinates(x=x, y=y + self.amount)

        return Coordinates(x=x, y=y - self.amount)  # Down

    @cached_property
    def moving_horizontal(self) -> bool:
        return self.direction in (Direction.LEFT, Direction.RIGHT)

    @cached_property
    def moving_vertical(self) -> bool:
        return self.direction in (Direction.UP, Direction.DOWN)

    def check_bounds(self, width: int, height: int) -> bool:
        if self.direction == Direction.LEFT:
            return self.new_coordinates.x >= 0
        elif self.direction == Direction.RIGHT:
            return self.new_coordinates.x <= width - self.amount * 2
        elif self.direction == Direction.UP:
            return self.new_coordinates.y >= self.amount * 4
        elif self.direction == Direction.DOWN:
            return self.new_coordinates.y <= height - self.amount * 4

        return False

    def check_proximity(self, coordinates: Coordinates) -> bool:
        is_near = self.new_coordinates.x in self._make_range(
            coordinates.x
        ) and self.new_coordinates.y in self._make_range(coordinates.y, multiplier=4)

        if is_near:
            # Only matters if moving towards it
            if self.direction == Direction.LEFT:
                return self.new_coordinates.x > coordinates.x
            elif self.direction == Direction.RIGHT:
                return self.new_coordinates.x < coordinates.x
            elif self.direction == Direction.UP:
                return self.new_coordinates.y > coordinates.y
            elif self.direction == Direction.DOWN:
                return self.new_coordinates.y < coordinates.y

        return is_near

    def _make_range(self, value: int, multiplier: int = 1):
        return range(value - self.amount * multiplier, value + self.amount * multiplier)


class CollisionDetector:
    def __init__(self, display: GameDisplay):
        self.display = display

    def can_move(self, request: MotionRequest) -> bool:
        return self._is_in_bounds(request) and self._is_clear_from_monsters(request)

    def _is_in_bounds(self, request: MotionRequest) -> bool:
        return request.check_bounds(self.display.width, self.display.height)

    def _is_clear_from_monsters(self, request: MotionRequest) -> bool:
        return not any(request.check_proximity(m) for m in self.display.beacon.monsters.values())
