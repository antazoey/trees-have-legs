from pygame.event import Event
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.constants import Views
from pharcobial.logging import game_logger
from pharcobial.managers.base import ManagerAccess, ViewController
from pharcobial.sprites.base import NPC, BaseSprite
from pharcobial.sprites.bubble import ChatBubble
from pharcobial.sprites.player import Player
from pharcobial.utils.timer import VisibilityTimer


class CameraGroup(Group):
    def __init__(self, surface: Surface) -> None:
        super().__init__()
        self.surface = surface

    def draw_in_view(self, offset: Vector2):
        top_layer_types = (Player, NPC, ChatBubble)
        top_layer = []
        for sprite in sorted(self.sprites(), key=lambda s: s.rect is not None and s.rect.centery):
            assert isinstance(sprite, BaseSprite)  # for Mypy
            if not sprite.visible:
                continue

            # Mypy doesn't realize this is valid.
            offset_pos: Vector2 = sprite.rect.topleft - offset  # type: ignore[operator]
            if any(isinstance(sprite, t) for t in top_layer_types):
                top_layer.append((sprite.image, offset_pos))
            else:
                # Draw ground layer
                self.surface.blit(sprite.image, offset_pos)

        for img, offset in top_layer:
            self.surface.blit(img, offset)


class Camera(ManagerAccess):
    def __init__(self) -> None:
        super().__init__()
        self.offset = Vector2()
        self.followee: BaseSprite | None = None

    def update(self):
        if self.followee is not None:
            self.offset.x = self.followee.rect.centerx - self.display.half_width
            self.offset.y = self.followee.rect.centery - self.display.half_height


class EndScreen(ManagerAccess):
    def __init__(self) -> None:
        self.visible: bool = False
        self.total_frames = 75
        self.timer = VisibilityTimer(amount=self.total_frames)
        self.gfx_id = ""

    @property
    def frames_left(self) -> int:
        return self.timer.timer or 0

    def win(self):
        self.gfx_id = "you-won"
        self.visible = True

    def lose(self):
        self.gfx_id = "you-died"
        self.visible = True

    def update(self):
        self.timer.update(self)

    def draw(self):
        if self.visible:
            transparent = self.frames_left < 0.25 * self.total_frames
            self.display.show_graphic(self.gfx_id, "center", scale=8, transparent=transparent)


class WorldManager(ViewController):
    def __init__(self) -> None:
        super().__init__(Views.WORLD, CameraGroup(self.display.active.screen))
        self.camera = Camera()
        self.group: CameraGroup = self.group
        self.end_screen = EndScreen()

    def validate(self):
        assert self.group is not None
        assert self.camera is not None
        game_logger.debug("World ready.")

    def handle_event(self, event: Event):
        # NOTE: Player events are handled in the Controller.
        self.sprites.player.handle_event(event)

    def update(self):
        self.camera.update()
        self.group.update()
        self.hud.update()
        self.end_screen.update()

    def draw(self):
        if self.end_screen.frames_left < 0.25 * self.end_screen.total_frames:
            self.group.draw_in_view(self.camera.offset)
            self.hud.draw()

        self.end_screen.draw()

    def follow(self, sprite: BaseSprite):
        self.camera.followee = sprite


world_manager = WorldManager()
