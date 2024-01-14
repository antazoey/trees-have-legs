from pygame import Surface

from treeshavelegs.constants import Graphics
from treeshavelegs.sprites.base import InGameItem, Interactive, WorldSprite
from treeshavelegs.types import SpriteID
from treeshavelegs.utils.timer import VisibilityTimer


class ChatBubble(InGameItem):
    """
    A chat bubble that appears near the player.
    """

    def __init__(self, parent: WorldSprite) -> None:
        self.image: Surface

        super().__init__(
            "chat-bubble",
            Graphics.CHAT_BUBBLE,
            (parent.camera_group,),
            position=parent.rect.inflate((0, -5)).topleft,
            hitbox_inflation=(0, 0),
        )
        self.parent_id: SpriteID = parent.sprite_id
        self.visible: bool = False
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
            if sprite.sprite_id != "runner" or not self.sprites[self.parent_id].is_accessible(
                self.sprites.runner, scalar=4
            ):
                continue

            # Activate sprite.
            assert isinstance(sprite, Interactive)  # for mypy
            sprite.handle_activate(self)
