from pharcobial.sprites.base import MobileSprite


class ChatBubble(MobileSprite):
    """
    A chat bubble that appears near the player.
    """

    def __init__(self, parent: MobileSprite) -> None:
        super().__init__(parent.rect.topleft, "chat-bubble", (parent.camera_group,), (0, 0))
        self.parent_id = parent.get_sprite_id()
        self.visible = False

    def get_sprite_id(self) -> str:
        return f"{self.parent_id}-bubble"
