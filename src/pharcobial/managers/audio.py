from pharcobial.managers.base import BaseManager

from pharcobial.utils.paths import game_paths
from pygame import mixer


class AudioManager(BaseManager):
    def __init__(self):
        self.theme = mixer.music.load(str(game_paths.sfx / "theme.ogg"))
        self.playing_music = False

    def update(self):
        if not self.playing_music:
            mixer.music.play(-1)  # -1 means loop forever.
            self.playing_music = True


audio_manager = AudioManager()
