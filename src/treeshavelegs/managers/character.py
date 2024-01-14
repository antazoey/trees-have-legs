from dataclasses import dataclass

from treeshavelegs.constants import DEFAULT_AP, DEFAULT_HP, DEFAULT_MAX_HP
from treeshavelegs.managers.base import BaseManager
from treeshavelegs.types import GfxID


@dataclass
class CharacterData:
    character_id: str
    gfx_id: GfxID
    max_speed: int = 128
    hp: int = DEFAULT_HP
    max_hp: int = DEFAULT_MAX_HP
    ap: int = DEFAULT_AP

    @classmethod
    def from_id(cls, character_id: str) -> "CharacterData":
        return cls(character_id=character_id, gfx_id=character_id)


class CharacterManager(BaseManager):
    JULES = "jules"
    TAYLOR = "taylor"
    LESTER = "lester"
    JOSH = "josh"

    def __init__(self) -> None:
        super().__init__()
        self.character_map = {
            self.JULES: CharacterData.from_id(self.JULES),
            self.TAYLOR: CharacterData.from_id(self.TAYLOR),
            self.LESTER: CharacterData.from_id(self.LESTER),
            self.JOSH: CharacterData.from_id(self.JOSH),
        }

        # Initial roles.
        self.active_character_id: str = self.JULES
        self.runner_id: str = self.TAYLOR

    def __getitem__(self, character_id: str) -> CharacterData:
        return self.character_map[character_id]

    def change_character(self, character: str):
        self.active_character_id = character

    def change_runner(self, character: str):
        self.runner_id = character

    @property
    def active_character(self) -> CharacterData:
        return self.character_map[self.active_character_id]

    @property
    def runner(self) -> CharacterData:
        return self.character_map[self.runner_id]


character_manager = CharacterManager()
