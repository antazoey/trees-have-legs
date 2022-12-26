from functools import cached_property
from typing import Dict, Iterable, List

from pygame.event import Event

from pharcobial.constants import MAP_VOID, Maps
from pharcobial.logging import game_logger
from pharcobial.managers.base import BaseManager
from pharcobial.sprites.base import NPC, BaseSprite
from pharcobial.sprites.bush import Bush
from pharcobial.sprites.player import Player
from pharcobial.sprites.tile import Ground, Tile, Void
from pharcobial.types import MapID, Position, SpriteID


class SpriteManager(BaseManager):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_cache: Dict[str, BaseSprite] = {}

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
        player = Player((self.world.group, self.collision.group))
        self._sprite_cache[player.sprite_id] = player
        return player

    @cached_property
    def tiles(self) -> List[Tile]:
        return [
            Void(Position.parse_coordinates(x=x, y=y), (self.world.group, self.collision.group))
            if tile_key == MAP_VOID
            else Ground(Position.parse_coordinates(x=x, y=y), tile_key, (self.world.group,))
            for y, row in enumerate(self.map)
            for x, tile_key in enumerate(row)
        ]

    @cached_property
    def npcs(self) -> List[NPC]:
        npc_list: List[NPC] = []
        for npc, pos in self.map.npcs_start:
            if npc.startswith("bush-"):
                index = npc.replace("bush-", "").strip()
                bush = Bush(pos, index, (self.world.group, self.collision.group))
                npc_list.append(bush)

        return npc_list

    @property
    def all_sprites(self) -> Iterable[BaseSprite]:
        yield self.player

        for npc in self.npcs:
            yield npc

        for tile in self.tiles:
            yield tile

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


sprite_manager = SpriteManager()
