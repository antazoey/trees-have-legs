from functools import cached_property
from importlib import import_module
from typing import Dict, Iterable, List, Type

from pygame.event import Event

from pharcobial.constants import MAP_VOID, Graphics, Maps
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import NPC, BaseSprite
from pharcobial.sprites.player import Player
from pharcobial.sprites.taylor import Taylor
from pharcobial.sprites.tile import Ground, Tile, Void
from pharcobial.types import MapID, Position, Positional, SpriteID


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[SpriteID, BaseSprite] = {}
        self.npc_start_positions: Dict[SpriteID, Positional] = {}

    def init_level(self, map_id: MapID):
        """
        Create the sprites needed for the given map ID.
        """

        assert map_id == Maps.BUFFER_PROPERTY  # Currently only one.
        _ = self.player
        _ = self.npcs
        _ = self.tiles

    def dict(self) -> Dict:
        return {
            "player": self.player.dict(),
            "npcs": [x.dict() for x in self.npcs],
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
    def npcs(self) -> List[NPC]:
        npc_list: List[NPC] = []
        for npc, pos in self.map.npcs_start:
            npc_cls = _sprite_id_to_npc_cls(npc)

            # NOTE: These kwargs are likely overriden in certain NPC classes
            # some of these values act as "defaults".
            npc_obj = npc_cls(
                sprite_id=npc,
                position=pos,
                gfx_id=npc,
                groups=(self.world.group, self.collision.group),
                hitbox_inflation=None,
            )
            self.npc_start_positions[npc] = pos
            npc_list.append(npc_obj)

        return npc_list

    @property
    def all_sprites(self) -> Iterable[BaseSprite]:
        yield self.player

        for npc in self.npcs:
            yield npc

        for tile in self.tiles:
            yield tile

    def reset(self):
        self.player.force_move(self.map.player_start)
        for npc in self.npcs:
            npc.force_move(self.npc_start_positions[npc.sprite_id])

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


def _sprite_id_to_npc_cls(sprite_id: SpriteID) -> Type[NPC]:
    parts = sprite_id.split("-")
    if parts[-1].isnumeric():
        parts = parts[:-1]

    mod_name = "_".join(x for x in parts)
    cls_name = "".join([x.capitalize() for x in parts])
    module = import_module(f"{ROOT_SPRITE_MODULE}.{mod_name}")
    return getattr(module, cls_name)


sprite_manager = SpriteManager()
