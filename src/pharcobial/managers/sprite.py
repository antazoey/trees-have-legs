from functools import cached_property
from importlib import import_module
from typing import Dict, Iterable, List, Type

from pygame.event import Event

from pharcobial.constants import MAP_VOID, Graphics, Maps
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import BaseSprite, WorldSprite
from pharcobial.sprites.player import Player
from pharcobial.sprites.taylor import Taylor
from pharcobial.sprites.tile import Ground, Tile, Void
from pharcobial.types import MapID, Position, Positional, SpriteID


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[SpriteID, BaseSprite] = {}
        self.world_sprite_start_positions: Dict[SpriteID, Positional] = {}

    def init_level(self, map_id: MapID):
        """
        Create the sprites needed for the given map ID.
        """

        assert map_id == Maps.BUFFER_PROPERTY  # Currently only one.
        _ = self.player
        _ = self.world_sprites
        _ = self.tiles

    def dict(self) -> Dict:
        return {
            "player": self.player.dict(),
            "world_sprites": [x.dict() for x in self.world_sprites],
            "tiles": [x.dict() for x in self.tiles],
        }

    def validate(self):
        assert self.player
        game_logger.debug("Sprites ready.")

    @cached_property
    def player(self) -> Player:
        player = Player()
        self._sprite_cache[player.sprite_id] = player
        return player

    @cached_property
    def taylor(self) -> Taylor:
        taylor = self.sprites[Graphics.TAYLOR]
        assert isinstance(taylor, Taylor)
        return taylor

    @cached_property
    def tiles(self) -> List[Tile]:
        return [
            Void(Position.parse_coordinates(x=x, y=y))
            if tile_key == MAP_VOID
            else Ground(
                Position.parse_coordinates(x=x, y=y),
                tile_key,
                self.map.tile_set[tile_key].get("collision", False),
            )
            for y, row in enumerate(self.map)
            for x, tile_key in enumerate(row)
        ]

    @cached_property
    def world_sprites(self) -> List[WorldSprite]:
        sprite_list: List[WorldSprite] = []
        for sprite_id, pos in self.map.start_positions:
            sprite_cls = _sprite_id_to_cls(sprite_id)

            # NOTE: These kwargs are likely overriden in certain sub-classes
            # some of these values act as "defaults".
            sprite = sprite_cls(
                sprite_id=sprite_id,
                position=pos,
                gfx_id=sprite_id,
                groups=(self.world.group, self.collision.group),
                hitbox_inflation=None,
            )
            self.world_sprite_start_positions[sprite_id] = pos
            sprite_list.append(sprite)

        return sprite_list

    @property
    def all_sprites(self) -> Iterable[BaseSprite]:
        yield self.player

        for npc in self.world_sprites:
            yield npc

        for tile in self.tiles:
            yield tile

    def reset(self):
        self.player.force_move(self.map.player_start)
        for sprite in self.world_sprites:
            sprite.force_move(self.world_sprite_start_positions[sprite.sprite_id])

    def __getitem__(self, key: SpriteID) -> BaseSprite:
        if key in self._sprite_cache:
            return self._sprite_cache[key]

        # Brute force find it and cache it
        for sprite in self.all_sprites:

            if sprite.sprite_id == key:
                # This sprite is likely requested often.
                # Cache for faster look-up next time.
                self._sprite_cache[sprite.sprite_id] = sprite
                return sprite

        raise IndexError(f"Sprite with ID '{key}' not found.")

    def handle_event(self, event: Event):
        self.player.handle_event(event)


ROOT_SPRITE_MODULE = ".".join(BaseSprite.__module__.split(".")[:-1])


def _sprite_id_to_cls(sprite_id: SpriteID) -> Type[WorldSprite]:
    parts = sprite_id.split("-")
    if parts[-1].isnumeric():
        parts = parts[:-1]

    mod_name = "_".join(x for x in parts)
    cls_name = "".join([x.capitalize() for x in parts])
    module = import_module(f"{ROOT_SPRITE_MODULE}.{mod_name}")
    return getattr(module, cls_name)


sprite_manager = SpriteManager()
