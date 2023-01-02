from functools import cached_property
from typing import Callable, Dict, Iterable, Union

from pygame import BLEND_RGBA_MULT, SRCALPHA
from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

from pharcobial.constants import BLOCK_SIZE, DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP, RGB
from pharcobial.logging import game_logger
from pharcobial.managers.base import ManagerAccess
from pharcobial.types import Collision, GfxID, Locatable, Position, Positional, SpriteID


class BaseSprite(Sprite, ManagerAccess):
    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | str,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
        width: int = BLOCK_SIZE,
        height: int = BLOCK_SIZE,
    ) -> None:
        super().__init__()
        self.sprite_id = sprite_id
        self.gfx_id = gfx_id

        self.image: Surface = (
            self.graphics.get_filled_surface(gfx_id, width=width, height=height)
            if gfx_id in RGB
            else self.graphics[gfx_id]
        )
        self.rect: Rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitbox_inflation) if hitbox_inflation else self.rect
        self.visible = True

        for group in groups:
            group.add(self)

    @property
    def x(self) -> int:
        return self.hitbox.x

    @property
    def y(self) -> int:
        return self.hitbox.y

    @property
    def position(self) -> Position:
        return Position(*self.hitbox.topleft)

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

    def is_reachable(self, obj: Union[Rect, "BaseSprite"], scalar: float = 1.1) -> bool:
        rect = obj.hitbox if isinstance(obj, BaseSprite) else obj
        new_width = round(scalar * rect.width)
        new_height = round(scalar * rect.height)
        scaled_rect = rect.inflate(new_width - rect.width, new_height - rect.height)
        return self.hitbox.colliderect(scaled_rect)


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
    def __init__(self, prefix: GfxID, rate_fn: Callable) -> None:
        self.prefix = prefix
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

        return f"{self.prefix}{suffix}"


class MobileSprite(BaseSprite):
    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | str,
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
        if not self.gfx_id:
            return None

        if self.stopped:
            # Return a standing-still graphic of the last direction facing.
            image = self.graphics.get(self.gfx_id, flip_x=self.forward.x > 0)
            return image or self.image

        gfx_id = self.walk_animation.get_gfx_id()
        flip = self.forward.x > 0
        graphic = self.graphics.get(gfx_id, flip_x=flip)
        return graphic or self.image

    def walk_towards(self, obj: Locatable) -> Collision:
        position = Position.from_obj(obj)
        self.face(position)
        return self.walk(limit=position)

    def walk(self, limit: Locatable | None = None) -> Collision:
        if limit is not None:
            limit = Position.from_obj(limit)

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

            if limit:
                if (new_x < self.hitbox.x and new_x < limit.x) or (
                    new_x > self.hitbox.x and new_x > limit.x
                ):
                    new_x = limit[0]
                if (new_y < self.hitbox.y and new_y < limit.y) or (
                    new_y > self.hitbox.y and new_y > limit.y
                ):
                    new_y = limit[1]

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

    def force_move(self, position: Positional):
        self.hitbox.topleft = (*position,)  # type: ignore
        self.rect.center = self.hitbox.center

    def face(self, obj: Locatable):
        """
        Move this sprite towards the given sprite, based on its movement ability.
        Returns ``True`` if collided.
        """

        position = Position.from_obj(obj)
        # Handle x
        if position.x > self.hitbox.x:
            self.direction.x = 1
        elif position.x < self.hitbox.x:
            self.direction.x = -1

        # Handle y
        if position.y > self.hitbox.y:
            self.direction.y = 1
        elif position.y < self.hitbox.y:
            self.direction.y = -1

        if self.direction.magnitude() not in (0, 1):
            self.direction.normalize_ip()

        magnitude = self.direction.magnitude()
        if magnitude not in (0, 1):
            self.direction.normalize_ip()
            self.forward = self.direction.copy()
        elif magnitude != 0:
            self.forward = self.direction.copy()

    def follow(self, sprite: "MobileSprite"):
        self.max_speed = sprite.max_speed

        if not self.hitbox.colliderect(sprite.hitbox.inflate(BLOCK_SIZE, BLOCK_SIZE)):
            behind_vector = -self.sprites.player.forward
            x_behind = behind_vector.x * BLOCK_SIZE + self.sprites.player.x
            y_behind = behind_vector.y * BLOCK_SIZE + self.sprites.player.y
            self.walk_towards((x_behind, y_behind))
        else:
            self.ease.reset()
            self.image = self.graphics.get(self.sprite_id, flip_x=self.forward.x > 0) or self.image


class InGameItem(MobileSprite):
    pass


class DamageBlinker:
    def __init__(self, target: "Character"):
        self.target = target
        self.on = False

        self.interval_length = 5
        self.interval = 0
        self.num_blinks = 1
        self.blink_index = 0
        self.on_blink = True

    def update(self):
        if not self.on or self.blink_index == self.num_blinks:
            self.on = False
            self.reset()
            return

        elif self.on_blink and self.interval < self.interval_length:
            # Blink overlay remains on.
            self.interval += 1

            # Blink.
            image_copy = self.target.image.copy()
            alpha_surface = Surface(image_copy.get_size(), SRCALPHA)
            alpha_surface.fill((*RGB["red"], 90))
            image_copy.blit(alpha_surface, (0, 0), special_flags=BLEND_RGBA_MULT)
            self.target.image = image_copy

        elif self.on_blink and self.interval >= self.interval_length:
            # Blink overlay turns off.
            self.on_blink = False
            self.interval = 0
            self.blink_index += 1

        elif not self.on_blink and self.interval < self.interval_length:
            # Blink overlay remains off.
            self.interval += 1

        elif not self.on_blink and self.interval >= self.interval_length:
            # Blink overlay turns on.
            self.on_blink = True
            self.interval = 0

    def reset(self):
        self.blink_index = 0
        self.interval = 0
        self.on_blink = True


class Character(MobileSprite):
    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | str,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ) -> None:
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation)
        self.hp = hp
        self.max_hp = max_hp
        self.ap = ap
        self.damage_blinker = DamageBlinker(self)

    def deal_damage(self, other: "Character"):
        other.handle_attack(self.ap)

    def handle_attack(self, ap: float | int):
        self.hp -= round(ap)
        if self.hp <= 0:
            self.die()

        self.damage_blinker.on = True

    def die(self):
        game_logger.debug(f"'{self.sprite_id}' died.")
        self.damage_blinker.reset()


class NPC(Character):
    """
    A non-player character.
    """

    def __init__(
        self,
        sprite_id: SpriteID,
        position: Positional,
        gfx_id: GfxID | str,
        groups: Iterable[AbstractGroup],
        hitbox_inflation: Positional | None,
        hp: int = DEFAULT_HP,
        max_hp: int = DEFAULT_MAX_HP,
        ap: int = DEFAULT_AP,
    ) -> None:
        super().__init__(sprite_id, position, gfx_id, groups, hitbox_inflation, hp, max_hp, ap)


WorldSprite = Union[InGameItem, Character]
WORLD_SPRITE_TYPES = (InGameItem, Character)


__all__ = ["BaseSprite", "InGameItem", "MobileSprite", "NPC", "WorldSprite"]
