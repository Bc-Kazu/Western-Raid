''' ============================================================= '''
from random import choice

''' ========= HANDLING EVERYTHING IN THE LOADING SCREEN  ======== '''
''' ============================================================= '''

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class Loading(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.loading_dots = '.'
        self.dots_tick = 0

        self.loading_tick = 0
        self.loading_interval = 120
        self.loading_tips = [
            'Use + or - keys to change music volume!',
            'Use [ or ] keys to change sound effect volume!',
            'Press 0 to mute/unmute music!',
            'Hold ESC in round to return to menu!',
            'Press BACKSPACE on menu to remove players!',
        ]

    def draw(self, game):
        game.screen.fill(colors.space_blue)

        if game.title_name == '< WESTERN RAID >':
            game.stars.update(game)
        else:
            game.win_stars.update(game)

        self.loading_tick += 1
        self.dots_tick += 1

        if self.dots_tick >= 30:
            self.dots_tick = 0
            self.loading_dots += '.'

            if len(self.loading_dots) > 3:
                self.loading_dots = '.'

            game.text.loading.set_text('Loading' + self.loading_dots)

        if self.loading_tick == 1:
            game.text.loading_tip.set_text(choice(self.loading_tips))
            game.load_level()

        game.text.loading.draw(game)
        game.text.loading_tip.draw(game)

        if self.loading_tick > self.loading_interval:
            game.start_round()