from typing import Callable, Iterable

from pygame.math import Vector2
from pygame.sprite import Group

from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite


class CameraGroup(Group):
    def draw_in_view(self, offset: Vector2, draw_fn: Callable):
        for sprite in sorted(self.sprites(), key=lambda s: s.rect is not None and s.rect.centery):
            rect = sprite.rect
            if not rect:
                # Should not happen, but for type-safety.
                continue

            # TODO: Figure out typing issue here.
            offset_pos = rect.topleft - offset  # type: ignore
            draw_fn(sprite.image, offset_pos)


class CameraManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.offset = Vector2()
        self.group = CameraGroup()
        self.followee = self.sprites.player

    def extend(self, sprites: Iterable[BaseSprite]):
        """
        Add all the environment sprit
        """

        for sprite in sprites:
            self.group.add(sprite)

    def add(self, sprite: BaseSprite):
        self.group.add(sprite)

    def update(self):
        self.offset.x = self.followee.rect.centerx - self.display.width // 2
        self.offset.y = self.followee.rect.centery - self.display.height // 2
        self.group.update()

    def draw(self):
        self.group.draw_in_view(self.offset, self.display.active.draw_surface)


camera_manager = CameraManager()
