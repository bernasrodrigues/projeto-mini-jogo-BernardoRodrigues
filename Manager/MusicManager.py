import os

from pygame import mixer

from Subject_Observer.Subject import Subject
from Subject_Observer.created_events import POINT_EVENT, DEATH_EVENT


class MusicManager(Subject):
    __instance = None

    @staticmethod
    def getInstance() -> __instance:
        if MusicManager.__instance is None:
            MusicManager()
        return MusicManager.__instance

    def __init__(self):
        super().__init__()
        if MusicManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.volume = 0.5

            mixer.init()
            # Background theme mixer
            self.theme = mixer.Channel(0)
            sound = mixer.Sound(os.path.join('Sounds/', "theme.wav"))
            self.theme.set_volume(self.volume)
            self.theme.play(sound, loops=-1)

            # Sound effects mixer
            self.channel = mixer.Channel(1)
            self.channel.set_volume(self.volume)

            MusicManager.__instance = self

    def notify(self, event):

        if event.type == POINT_EVENT:
            sound = mixer.Sound(os.path.join('Sounds/', "pickup.wav"))
            self.channel.play(sound)

        elif event.type == DEATH_EVENT:
            self.theme.pause()
            sound = mixer.Sound(os.path.join('Sounds/', "death_sound.wav"))
            self.channel.play(sound)
