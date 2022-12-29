from pharcobial.sprites.base import NPC


class Taylor(NPC):
    def __init__(self):
        super().__init__(
            "taylor",
            (200, 300),
            "taylor",
            (self.world.group, self.collision.group),
            (-10, -20),
        )

    def update(self, *args, **kwargs) -> None:
        self.move((200, 200))
