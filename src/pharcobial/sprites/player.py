import pygame  # type: ignore

from pharcobial._types import Orientation
from pharcobial.constants import BLOCK_SIZE
from pharcobial.managers.graphics import graphics_manager
from pharcobial.sprites.base import BaseSprite


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(self, init_x: int, init_y: int, character: str = "pharma"):
        super().__init__()
        self.character = character
        self.move_gfx_id: int = -1
        self.speed = 0.24
        self.uses_events: bool = True
        self.orientation: Orientation = Orientation.LEFT

        self.keys_down = {
            Orientation.LEFT: False,
            Orientation.RIGHT: False,
            Orientation.UP: False,
            Orientation.DOWN: False,
        }

        self.image = graphics_manager[self.character]
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y

    @property
    def moving(self) -> bool:
        for orientation in [d for d, v in self.keys_down.items() if v]:
            if orientation == Orientation.LEFT:
                return not self.keys_down[Orientation.RIGHT]
            elif orientation == Orientation.RIGHT:
                return not self.keys_down[Orientation.LEFT]
            elif orientation == Orientation.UP:
                return not self.keys_down[Orientation.DOWN]
            elif orientation == Orientation.DOWN:
                return not self.keys_down[Orientation.UP]

        return False

    def get_sprite_id(self) -> str:
        return "player"

    def get_gfx_id(self) -> str:
        if not self.moving:
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

        return f"{self.character}{suffix}"

    def handle_event(self, event):
        """
        Handle when a user presses a key. If the user holds a key,
        the character continuously moves that direction. This method
        gets called once for the event whereas ``move()`` gets called
        every game loop.
        """
        key_map = {
            pygame.K_LEFT: Orientation.LEFT,
            pygame.K_RIGHT: Orientation.RIGHT,
            pygame.K_UP: Orientation.UP,
            pygame.K_DOWN: Orientation.DOWN,
        }
        if event.type == pygame.KEYDOWN and event.key in key_map:
            # Start moving
            self.keys_down[key_map[event.key]] = True

        elif event.type == pygame.KEYUP and event.key in key_map:
            # Stop moving
            self.keys_down[key_map[event.key]] = False

        # NOTE: Always handle LEFT / RIGHT before UP / DOWN
        # to prevent walking backwards for combos like UP + RIGHT
        if self.keys_down[Orientation.LEFT]:
            self.orientation = Orientation.LEFT
        elif self.keys_down[Orientation.RIGHT]:
            self.orientation = Orientation.RIGHT
        elif self.keys_down[Orientation.UP]:
            self.orientation = Orientation.LEFT
        elif self.keys_down[Orientation.DOWN]:
            self.orientation = Orientation.RIGHT

    def update(self, *args, **kwargs):
        # NOTE: Set image before exiting early when not moving
        # to get the correct standing-still image.
        gfx_id = self.get_gfx_id()
        self.image = graphics_manager.get(gfx_id, orientation=self.orientation)

        if not self.moving:
            return

        length = BLOCK_SIZE * self.speed
        x = 0
        y = 0

        # Update potential movement
        if self.keys_down[Orientation.LEFT]:
            x -= 1
        if self.keys_down[Orientation.RIGHT]:
            x += 1
        if self.keys_down[Orientation.UP]:
            y -= 1
        if self.keys_down[Orientation.DOWN]:
            y += 1

        # Set image
        new_x = round(self.rect.x + x * length)
        new_y = round(self.rect.y + y * length)

        # Adjust coordinates. Note: must happen after setting image.
        self.move(new_x, new_y)
