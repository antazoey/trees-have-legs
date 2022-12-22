from typing import Iterable

from pygame.math import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite


class CameraGroup(Group):
    def __init__(self, surface: Surface) -> None:
        super().__init__()
        self.surface = surface

    def draw_in_view(self, offset: Vector2):
        for sprite in sorted(self.sprites(), key=lambda s: s.rect is not None and s.rect.centery):
            rect = sprite.rect
            image = sprite.image
            if not rect or not image:
                # Should not happen, but for type-safety.
                continue

            # Mypy doesn't realize this is valid.
            offset_pos: Vector2 = rect.topleft - offset  # type: ignore[operator]
            self.surface.blit(image, offset_pos)


class CameraManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self.offset = Vector2()
        self.group = CameraGroup(self.display.active.screen)
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
        self.group.draw_in_view(self.offset)


camera_manager = CameraManager()
