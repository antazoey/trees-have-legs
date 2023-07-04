import logging

game_logger = logging.getLogger("trees-have-legs")
game_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
game_logger.addHandler(handler)


__all__ = ["game_logger"]
