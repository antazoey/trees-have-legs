from functools import cached_property
from typing import Callable, Dict, Iterable

from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

from pharcobial.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP
from pharcobial.logging import game_logger
from pharcobial.managers.base import ManagerAccess
from pharcobial.types import Collision, GfxID, Positional, SpriteID


class BaseSprite(Sprite, ManagerAccess):
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

    def set_image(self, gfx: GfxID):
        if self.gfx_id != gfx:
            self.image = self.graphics[gfx]
            self.gfx_id = gfx

    def activated(self):
        """
        Handle the player activating you. Defaults to do nothing.
        """


class Ease:
    def __init__(self):
        self.forward = None
        self.start = 0.8
        self.effect = self.start
        self.slide_increment = 0.002
        self.slide_start = 0.02
        self.slide = self.slide_start
        self.last = "r"

    def _in(self):
        if self.last == "o":
            # Always enforce reset in between segments.
            self.reset()

        self.effect += self.slide
        self.slide += self.slide_increment
        self.last = "i"

    def out(self):
        if self.last == "i":
            # Always enforce reset in between segments.
            self.reset()

        self.effect -= self.slide
        self.slide += self.slide_increment
        self.last = "o"

    def reset(self):
        self.effect = self.start
        self.slide = self.slide_start
        self.last = "r"


class Walk:
    def __init__(self, sprite_id: SpriteID, rate_fn: Callable) -> None:
        self.sprite_id = sprite_id
        self.index = 0
        self.rate_fn = rate_fn

    def get_gfx_id(self) -> GfxID:
        self.index += 1
        rate = self.rate_fn()
        if self.index in range(rate):
            suffix = "-walk-1"
        elif self.index in range(rate, rate * 2 + 1):
            suffix = "-walk-2"
        else:
            suffix = ""
            self.index = -1

        return f"{self.sprite_id}{suffix}"


class MobileSprite(BaseSprite):
    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | None,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
    ) -> None:
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation)
        self.max_speed: float = 0
        self.direction = Vector2()
        self.forward = Vector2()
        self.ease = Ease()

    @cached_property
    def walk_animation(self) -> Walk:
        def get_rate():
            ease = self.ease.effect if self.accelerating else 1 / self.ease.effect
            return round(self.max_speed / 24 * ease)

        return Walk(self.sprite_id, get_rate)

    @property
    def speed(self) -> float:
        return self.max_speed * self.clock.deltatime

    @property
    def moving(self) -> bool:
        return round(self.direction.magnitude()) != 0

    @property
    def stopped(self) -> bool:
        return not self.moving and self.ease.effect <= self.ease.start

    @property
    def coming_to_stop(self) -> bool:
        return not self.moving and self.ease.effect > self.ease.start

    @property
    def accelerating(self) -> bool:
        return self.moving and self.ease.effect < 1

    def get_graphic(self) -> Surface | None:
        if self.stopped:
            # Return a standing-still graphic of the last direction facing.
            image = self.graphics.get(self.sprite_id, flip_x=self.forward.x > 0)
            return image or self.image

        gfx_id = self.walk_animation.get_gfx_id()
        flip = self.forward.x > 0
        graphic = self.graphics.get(gfx_id, flip_x=flip)
        return graphic or self.image

    def walk_towards(self, rect: Rect | BaseSprite) -> Collision:
        self.face(rect)
        return self.walk()

    def walk(self) -> Collision:
        self.image = self.get_graphic() or self.image

        if self.stopped:
            self.ease.reset()
            return Collision()

        elif self.coming_to_stop:
            new_x = self.hitbox.x + self.forward.x * self.speed * self.ease.effect
            new_y = self.hitbox.y + self.forward.y * self.speed * self.ease.effect

            if self.ease.effect > self.ease.start:
                self.ease.out()

        else:  # Start moving (Ease-in)
            new_x = self.hitbox.x + self.direction.x * self.speed * self.ease.effect
            new_y = self.hitbox.y + self.direction.y * self.speed * self.ease.effect
            if self.ease.effect < 1:
                self.ease._in()

        return self.move((new_x, new_y))

    def move(self, position: Positional) -> Collision:
        collided_x = collided_y = None
        changed_x = changed_y = False
        x, y = position
        x_rounded = round(x)
        y_rounded = round(y)
        if self.hitbox.x != x_rounded:
            pre_check = self.hitbox.x
            self.hitbox.x = x_rounded
            collided_x = self.collision.check_x(self)
            self.hitbox.x = pre_check
            changed_x = True

        if self.hitbox.y != y_rounded:
            pre_check = self.hitbox.y
            self.hitbox.y = y_rounded
            collided_y = self.collision.check_y(self)
            self.hitbox.y = pre_check
            changed_y = True

        changed = False
        if changed_x and not collided_y and not collided_x:
            self.hitbox.x = x_rounded
            changed = True
        if changed_y and not collided_x and not collided_y:
            self.hitbox.y = y_rounded
            changed = True

        if changed:
            self.rect.center = self.hitbox.center

        return Collision(x=collided_x, y=collided_y)

    def face(self, obj: Rect | BaseSprite):
        """
        Move this sprite towards the given sprite, based on its movement ability.
        Returns ``True`` if collided.
        """

        if isinstance(obj, BaseSprite):
            rect = obj.rect
        else:
            rect = obj

        # Handle x
        if rect.x > self.hitbox.x:
            self.direction.x = 1
        elif rect.x < self.hitbox.x:
            self.direction.x = -1

        # Handle y
        if rect.y > self.hitbox.y:
            self.direction.y = 1
        elif rect.y < self.hitbox.y:
            self.direction.y = -1

        if self.direction.magnitude() not in (0, 1):
            self.direction = self.direction.normalize()


class Character(MobileSprite):
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
            self.die()

    def die(self):
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
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation, hp, max_hp, ap)


__all__ = ["BaseSprite", "MobileSprite", "NPC"]
