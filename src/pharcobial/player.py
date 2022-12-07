import pygame  # type: ignore

from pharcobial._types import Direction
from pharcobial.basesprite import BaseSprite
from pharcobial.collision import CollisionDetector
from pharcobial.display import GameDisplay


class Player(BaseSprite):
    """
    The main character.
    """

    def __init__(
        self, display: GameDisplay, collision_detector: CollisionDetector, character: str = "pharma"
    ):
        super().__init__(display, collision_detector)
        self.character = character

        # Put in middle of screen
        self.x = display.width // 2
        self.y = display.height // 2

        self.moving = False
        self.move_image_id: int = 0
        self.speed = 0.3
        self.movement_x = 0
        self.movement_y = 0

        self.keys_down = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

    def draw(self):
        # self.clear_previous_spot()
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

            self.keys_down[self.facing] = True
            self.moving = self.can_move

        elif event.type == pygame.KEYUP:
            if event.key in key_map:
                self.keys_down[key_map[event.key]] = False
            # Stop moving
            # self.moving = False

    def move(self):
        movement_length = self.display.block_size * self.speed

        # Update potential movement
        if self.keys_down[Direction.LEFT]:
            self.movement_x -= 1
        if self.keys_down[Direction.RIGHT]:
            self.movement_x += 1
        if self.keys_down[Direction.UP]:
            self.movement_y -= 1
        if self.keys_down[Direction.DOWN]:
            self.movement_y += 1

        # Check if can move.
        self.moving = self.can_move
        if not self.moving:
            return

        if self.coordinates:
            self.previous_coordinates = self.coordinates

        self.x += round(self.movement_x * movement_length)
        self.y += round(self.movement_y * movement_length)

        # Reset movement.
        self.movement_x = 0
        self.movement_y = 0
