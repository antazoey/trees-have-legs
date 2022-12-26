from pharcobial.constants import Graphics
from pharcobial.sprites.base import MobileSprite


class ChatBubble(MobileSprite):
    """
    A chat bubble that appears near the player.
    """

    def __init__(self, parent: MobileSprite) -> None:
        super().__init__(
            "{self.parent_id}-bubble",
            parent.rect.inflate((0, -5)).topleft,
            Graphics.CHAT_BUBBLE,
            (parent.camera_group,),
            (0, 0),
        )
        self.parent_id = parent.sprite_id
        self.visible = False
        self.timer: int | None = None

    def update(self, *args, **kwargs):
        self.rect = self.sprites[self.parent_id].rect.inflate((0, -5))
        if self.visible and self.timer is None:
            # Chat bubble was activated. Set a timer to only show
            # for a brief moment.
            self.timer = 25  # frames

        elif self.visible and self.timer == 0:
            self.visible = False
            self.timer = None

        elif self.visible and self.timer is not None:
            self.timer -= 1
