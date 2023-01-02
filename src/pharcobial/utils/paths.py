from pathlib import Path

from pharcobial.constants import SOURCE_DIR
from pharcobial.types import FontName, GfxID, MapID


class GamePaths:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    @property
    def gfx(self) -> Path:
        return self.base_dir / "gfx"

    @property
    def maps(self) -> Path:
        return self.base_dir / "maps"

    @property
    def fonts(self) -> Path:
        return self.base_dir / "fonts"

    @property
    def sfx(self) -> Path:
        return self.base_dir / "sfx"

    def get_graphic(self, gfx_id: GfxID, ext: str = "png") -> Path:
        return self.gfx / f"{gfx_id}.{ext}"

    def get_map(self, map_id: MapID) -> Path:
        return self.maps / f"{map_id}.csv"

    def get_font(self, font_name: FontName) -> Path:
        return self.fonts / f"{font_name}.ttf"


game_paths = GamePaths(SOURCE_DIR)
