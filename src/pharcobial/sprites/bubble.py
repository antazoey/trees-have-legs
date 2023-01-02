from pharcobial.constants import Graphics
from pharcobial.sprites.base import InGameItem, WorldSprite
from pharcobial.utils.timer import VisibilityTimer


class ChatBubble(InGameItem):
    """
    A chat bubble that appears near the player.
    """

    def __init__(self, parent: WorldSprite) -> None:
        super().__init__(
            "{self.parent_id}-bubble",
            parent.rect.inflate((0, -5)).topleft,
            Graphics.CHAT_BUBBLE,
            (parent.camera_group,),
            (0, 0),
        )
        self.parent_id = parent.sprite_id
        self.visible = False
        self.timer = VisibilityTimer()

    def set_graphic(self, flip_x: bool):
        bubble = self.graphics.get(Graphics.CHAT_BUBBLE, flip_x=flip_x)
        self.image = bubble or self.image

    def update(self, *args, **kwargs):
        self.rect = self.sprites[self.parent_id].rect.inflate((0, -5))
        self.timer.update(self)

        if not self.visible:
            return

        for sprite in self.collision._sprites:
            if sprite.sprite_id != Graphics.TAYLOR or not self.sprites[self.parent_id].is_reachable(
                self.sprites.taylor, scalar=8
            ):
                continue

            # Activate sprite.
            sprite.activated()
