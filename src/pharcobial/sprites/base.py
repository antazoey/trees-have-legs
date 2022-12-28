from functools import cached_property
from typing import Dict, Iterable, Tuple, cast

from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.types import GfxID, Position, Positional, SpriteID


class BaseSprite(Sprite, BaseManager):
    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | None,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
    ) -> None:
        super().__init__()
        self.sprite_id = sprite_id
        self.gfx_id = gfx_id
        self.image: Surface = (
            self.graphics[gfx_id] if gfx_id else self.graphics.get_filled_surface("black")
        )
        self.rect: Rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitbox_inflation) if hitbox_inflation else self.rect
        self.visible = True

        for group in groups:
            group.add(self)

    @cached_property
    def camera_group(self) -> AbstractGroup:
        return [x for x in self.groups() if "camera" in type(x).__name__.lower()][0]

    def dict(self) -> Dict:
        """
        Get a stateful dictionary for reloading.
        """
        return {
            "sprite_id": self.sprite_id,
            "position": {"x": self.rect.x, "y": self.rect.y},
            "gfx_id": self.gfx_id,
        }

    def handle_event(self, event: Event):
        """
        Handle events from pygame.
        Method not required for inactive sprites.
        """
        return

    def set_image(self, gfx_id: GfxID):
        if self.gfx_id != gfx_id:
            self.image = self.graphics[gfx_id]
            self.gfx_id = gfx_id


class MobileSprite(BaseSprite):
    speed: float = 0
    direction: Vector2

    def move(self, position: Positional) -> Tuple[BaseSprite | None, BaseSprite | None]:
        collided_x = None
        collided_y = None
        changed = False
        x, y = position
        if self.hitbox.x != x:
            self.hitbox.x = x
            collided_x = self.collision.check_x(self)
            changed = True

        if self.hitbox.y != y:
            self.hitbox.y = y
            collided_y = self.collision.check_y(self)
            changed = True

        if changed:
            self.rect.center = self.hitbox.center

        return (collided_x, collided_y)

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0

    def follow(self, sprite: BaseSprite) -> Tuple[BaseSprite | None, BaseSprite | None]:
        """
        Move this sprite towards the given sprite, based on its movement ability.
        Returns ``True`` if collided.
        """
        return self.move_towards(sprite.hitbox.topleft)

    def move_towards(self, position: Positional) -> Tuple[BaseSprite | None, BaseSprite | None]:
        """
        Move this sprite towards the given coordinates.
        """
        new_position = Position(self.hitbox.x, self.hitbox.y)
        x, y = position

        # Handle x
        if x > self.hitbox.x:
            new_position.x = round(self.hitbox.x + min(self.speed, x - self.hitbox.x))
            self.direction.x = 1
        elif x < self.hitbox.x:
            new_position.x = round(self.hitbox.x - min(self.speed, self.hitbox.x - x))
            self.direction.x = -1

        # Handle y
        if y > self.hitbox.y:
            new_position.y = round(self.hitbox.y + min(self.speed, y - self.hitbox.y))
            self.direction.y = 1
        elif y < self.hitbox.y:
            new_position.y = round(self.hitbox.y - min(self.speed, self.hitbox.y - y))
            self.direction.y = -1

        return self.move(new_position)


class Character(MobileSprite):
    hp: int
    max_hp: int
    ap: int

    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | None,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
        hp: int,
        max_hp: int,
        ap: int,
    ) -> None:
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation)
        self.hp = hp
        self.max_hp = max_hp
        self.ap = ap

    def deal_damage(self, other: "Character"):
        other.handle_attack(self.ap)

    def handle_attack(self, ap: int):
        self.hp -= ap

        if self.hp <= 0:
            game_logger.debug(f"'{self.sprite_id}' died.")


class NPC(Character):
    """
    A non-player character.
    """

    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | None,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ) -> None:
        hp = hp or DEFAULT_HP
        hp
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation, hp, max_hp, ap)


__all__ = ["BaseSprite", "MobileSprite", "NPC"]
