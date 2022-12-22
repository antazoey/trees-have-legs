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
        pending = []
        for sprite in sorted(self.sprites(), key=lambda s: s.rect is not None and s.rect.centery):
            assert isinstance(sprite, BaseSprite)  # for Mypy

            # Mypy doesn't realize this is valid.
            offset_pos: Vector2 = sprite.rect.topleft - offset  # type: ignore[operator]

            # Draw player last
            sprite_id = sprite.get_sprite_id()
            if sprite_id == "player" or "adversary-" in sprite_id:
                pending.append((sprite.image, offset_pos))
            else:
                self.surface.blit(sprite.image, offset_pos)

        for img, offset in pending:
            self.surface.blit(img, offset)


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
