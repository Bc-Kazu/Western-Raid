''' ============================================================= '''
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
        self.loading_interval = 0

    def draw(self, game):
        game.screen.fill(colors.space_blue)
        game.stars.update(game)

        self.loading_interval += 1
        if self.loading_interval >= 30:
            self.loading_interval = 0
            self.loading_dots += '.'

            if len(self.loading_dots) > 3:
                self.loading_dots = '.'

            game.text.loading.set_text('Loading' + self.loading_dots)

        game.text.loading.draw(game)
        game.text.loading_tip.draw(game)
