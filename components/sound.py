import pygame as pg

class Sound:
    def __init__(self):
        pg.mixer.init()
        self.mute = False
        self.music_offset = 0.8
        self.sfx_offset = 0.5
        
        self.last_volume = self.music_offset
        self.last_sfx = self.sfx_offset

    def play(self, song, loop=0):
        pg.mixer.stop()

        pg.mixer.music.load(f'assets/music/{song}.mp3')
        pg.mixer.music.set_volume(self.music_offset)

        pg.mixer.music.play(loop)

    def play_sfx(self, sfx):
        sound = pg.mixer.Sound(f'assets/SFX/{sfx}.wav')
        sound.set_volume(self.sfx_offset)
        sound.play()

    def mute_music(self):
        self.mute = not self.mute
        if self.mute:
            self.last_volume = self.music_offset
            self.last_sfx = self.sfx_offset
            self.music_offset = 0
            self.sfx_offset = 0
        else:
            self.music_offset = self.last_volume
            self.sfx_offset = self.last_sfx

        pg.mixer.music.set_volume(self.music_offset)

    def change_volume(self, volume_change):
        if volume_change == 'increase' and self.music_offset < 1:
            self.music_offset = round(self.music_offset + 0.1, 2)
            pg.mixer.music.set_volume(self.music_offset)
        if volume_change == 'decrease' and self.music_offset > 0:
            self.music_offset = round(self.music_offset - 0.1, 2)
            pg.mixer.music.set_volume(self.music_offset)
        if self.music_offset < 0: self.music_offset = 0

    def change_volume_sfx(self, volume_change):
        if volume_change == 'increase' and self.sfx_offset < 1:
            self.sfx_offset = round(self.sfx_offset + 0.1, 2)
        if volume_change == 'decrease' and self.sfx_offset > 0:
            self.sfx_offset = round(self.sfx_offset - 0.1, 2)
        if self.sfx_offset < 0: self.sfx_offset = 0
