import pygame

from pharcobial._types import BaseSprite, Coordinates, Direction
from pharcobial.display import GameDisplay
from pharcobial.motion import MotionGranter, MotionRequest


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(
        self, display: GameDisplay, motion_granter: MotionGranter, character: str = "pharma"
    ):
        self.display = display
        self.motion_granter = motion_granter
        self.character = character

        # Put in middle of screen
        self.x = display.width // 2
        self.y = display.height // 2
        self.previous_coordinates: Coordinates | None = None

        self.facing = Direction.LEFT
        self.moving = False
        self.move_image_id: int = 0

        super().__init__()

    def draw(self):
        if self.previous_coordinates:
            size = self.display.block_size * 2
            self.display.draw_rect("white", self.previous_coordinates, width=size, height=size)

        image_id = self._get_image_id()
        self.display.draw_image(image_id, self.coordinates)
        self.display.beacon.player = self.coordinates

    def _get_image_id(self) -> str:
        suffix = (
            Direction.LEFT.value
            if self.facing in (Direction.LEFT, Direction.UP)
            else Direction.RIGHT.value
        )

        if self.moving and self.move_image_id != 1:
            self.move_image_id = 1
            suffix = f"{suffix}-walk-{self.move_image_id}"
        elif self.moving:
            self.move_image_id = 2
            suffix = f"{suffix}-walk-{self.move_image_id}"
        else:
            self.move_image_id = 0

        return f"{self.character}-{suffix}"

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """
        key_map = {
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
        }
        if event.type == pygame.KEYDOWN and event.key in key_map:
            # Start moving
            self.facing = key_map[event.key]
            self._handle_environment()

        elif event.type == pygame.KEYUP:
            # Stop moving
            self.moving = event.key not in list(key_map.keys())
            self.moving = False

    def _handle_environment(self) -> bool:
        request = MotionRequest(start_coordinates=self.coordinates, direction=self.facing)
        self.moving = self.motion_granter.can_move(request)
        return self.moving

    def move(self):
        if not self.moving or not self._handle_environment():
            return

        if self.coordinates:
            self.previous_coordinates = self.coordinates

        if self.facing == Direction.LEFT:
            self.x -= self.display.block_size
        elif self.facing == Direction.RIGHT:
            self.x += self.display.block_size
        elif self.facing == Direction.UP:
            self.y -= self.display.block_size
        elif self.facing == Direction.DOWN:
            self.y += self.display.block_size
