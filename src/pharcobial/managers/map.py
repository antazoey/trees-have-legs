class Map:
    # TODO
    width: int = 1_000  # Blocks
    height: int = 1_000  # Blocks


class MapManager:
    active_map = Map()


map_manager = MapManager()
