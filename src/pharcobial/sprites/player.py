import pygame  # type: ignore

from pharcobial._types import Direction, DrawInfo
from pharcobial.constants import BLOCK_SIZE
from pharcobial.sprites.base import BaseSprite


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(self, character: str = "pharma"):
        super().__init__()
        self.character = character
        self.move_gfx_id: int = -1
        self.speed = 0.24
        self.active_gfx_id: str | None = None
        self.uses_events: bool = True
        self.orientation: Direction = Direction.LEFT

        self.keys_down = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

    @property
    def moving(self) -> bool:
        for direction in [d for d, v in self.keys_down.items() if v]:
            # Ensure opposite direction isn't canceling out.
            if direction == Direction.LEFT:
                return not self.keys_down[Direction.RIGHT]
            elif direction == Direction.RIGHT:
                return not self.keys_down[Direction.LEFT]
            elif direction == Direction.UP:
                return not self.keys_down[Direction.DOWN]
            elif direction == Direction.DOWN:
                return not self.keys_down[Direction.UP]

        return False

    def get_sprite_id(self) -> str:
        return "player"

    def get_draw_info(self) -> DrawInfo:
        return DrawInfo(
            gfx_id=self._get_gfx_id(),
            rect=self.rect,
            orientation=self.orientation,
        )

    def _get_gfx_id(self) -> str:
        if not self.moving and self.active_gfx_id is not None:
            # Return a standing-still graphic of the last direction facing.
            return self.character

        self.move_gfx_id += 1
        frame_rate = round(self.speed * BLOCK_SIZE)
        if self.move_gfx_id in range(frame_rate):
            suffix = "-walk-1"
        elif self.move_gfx_id in range(frame_rate, frame_rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.move_gfx_id = -1

        self.active_gfx_id = f"{self.character}{suffix}"
        return self.active_gfx_id

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
            self.keys_down[key_map[event.key]] = True

        elif event.type == pygame.KEYUP and event.key in key_map:
            # Stop moving
            self.keys_down[key_map[event.key]] = False

        # NOTE: Always handle LEFT / RIGHT before UP / DOWN
        # to prevent walking backwards for combos like UP + RIGHT
        if self.keys_down[Direction.LEFT]:
            self.orientation = Direction.LEFT
        elif self.keys_down[Direction.RIGHT]:
            self.orientation = Direction.RIGHT
        elif self.keys_down[Direction.UP]:
            self.orientation = Direction.LEFT
        elif self.keys_down[Direction.DOWN]:
            self.orientation = Direction.RIGHT

    def update(self, *args, **kwargs):
        if not self.moving:
            return

        length = BLOCK_SIZE * self.speed
        left = 0
        top = 0

        # Update potential movement
        if self.keys_down[Direction.LEFT]:
            left -= 1
        if self.keys_down[Direction.RIGHT]:
            left += 1
        if self.keys_down[Direction.UP]:
            top -= 1
        if self.keys_down[Direction.DOWN]:
            top += 1

        new_left = round(self.rect.left + left * length)
        new_top = round(self.rect.top + top * length)
        self.move(new_left, new_top)
