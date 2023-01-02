from typing import Dict

from pygame import mixer

from pharcobial.managers.base import BaseManager
from pharcobial.types import SfxID
from pharcobial.utils.paths import game_paths


class AudioManager(BaseManager):
    def __init__(self):
        self.load_music("theme")
        self.playing_music = False
        self.sounds: Dict[SfxID, mixer.Sound] = {}
        self.channels: Dict[SfxID, mixer.Channel] = {}

    def update(self):
        """
        For handling changes in music (not Sounds).
        """
        if not self.options.disable_music and not self.playing_music:
            mixer.music.play(-1)  # -1 means loop forever.
            self.playing_music = True

        elif self.options.disable_music and self.playing_music:
            mixer.music.stop()
            self.playing_music = False

    def load_music(self, sfx_id: SfxID):
        mixer.music.load(str(game_paths.sfx / f"{sfx_id}.ogg"))

    def play_music(self, continuously: bool = True):
        arguments = (-1,) if continuously else []
        mixer.music.play(*arguments)

    def play_sound(self, sfx_id: SfxID):
        if self.options.disable_sfx:
            return

        if sfx_id not in self.channels:
            self.channels[sfx_id] = mixer.Channel(len(self.channels) + 1)

        channel = self.channels[sfx_id]

        # TODO: Do something like this to prevent too many samples running.
        # if channel.get_busy():
        #     return

        sound = self.load_sound(sfx_id)
        channel.play(sound)

    def load_sound(self, sfx_id: SfxID) -> mixer.Sound:
        if sfx_id not in self.sounds:
            self.sounds[sfx_id] = mixer.Sound(str(game_paths.sfx / f"{sfx_id}.ogg"))

        return self.sounds[sfx_id]


audio_manager = AudioManager()
