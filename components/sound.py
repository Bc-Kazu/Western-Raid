import pygame as pg

class Sound:
    def __init__(self):
        pg.mixer.init()
        self.mute = False
        self.volume_offset = 0.5
        self.sfx_offset = 0.5

    def play(self, song, loop=0):
        pg.mixer.stop()

        pg.mixer.music.load(f'assets/music/{song}.mp3')
        pg.mixer.music.set_volume(self.volume_offset)

        pg.mixer.music.play(loop)

    def play_sfx(self, sfx):
        sound = pg.mixer.Sound(f'assets/SFX/{sfx}.wav')
        sound.set_volume(self.sfx_offset)
        sound.play()

    def mute_music(self):
        self.mute = not self.mute
        self.volume_offset = 0 if self.mute else 0.5
        self.sfx_offset = 0 if self.mute else 0.5
        pg.mixer.music.set_volume(self.volume_offset * 0.5)

    def change_volume(self, volume_change):
        if volume_change == 'increase' and self.volume_offset < 1:
            self.volume_offset = round(self.volume_offset + 0.1, 2)
            pg.mixer.music.set_volume(self.volume_offset)
        if volume_change == 'decrease' and self.volume_offset > 0:
            self.volume_offset = round(self.volume_offset - 0.1, 2)
            pg.mixer.music.set_volume(self.volume_offset)
        if self.volume_offset < 0: self.volume_offset = 0

    def change_volume_sfx(self, volume_change):
        if volume_change == 'increase' and self.sfx_offset < 1:
            self.sfx_offset = round(self.sfx_offset + 0.1, 2)
        if volume_change == 'decrease' and self.sfx_offset > 0:
            self.sfx_offset = round(self.sfx_offset - 0.1, 2)
        if self.sfx_offset < 0: self.sfx_offset = 0
