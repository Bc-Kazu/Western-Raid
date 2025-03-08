''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE DEFEAT SCREEN  ========= '''
''' ============================================================= '''

from assets import DEFEAT_CAGE, DEFEAT_CAGE_RECT

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class Defeat(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()

    def draw(self, game):
        game.screen.fill(colors.sad_orange)
        game.text.lost_text.draw(game)
        game.text.full_score_text.rect = (265, 250)
        game.text.full_score_text.string = str("FINAL SCORE: {:07d}".format(game.data["total_score"]))
        game.text.full_score_text.draw(game)
        game.text.return_text.draw(game)

        # Draw defeat stats and players
        if game.player_2:
            game.player_1.set_offset([-50, 0], [-2, 2])
            game.player_2.set_offset([50, 0], [2, 2])
            game.player_2.draw(game)
            game.player_1.draw(game)
            game.player_1.set_eyes('closed_eyes')
            game.player_2.set_eyes('closed_eyes')
        elif game.player_1:
            game.player_1.set_offset(None, [-2, 2])
            game.player_1.draw(game)
            game.player_1.set_eyes('closed_eyes')

        game.screen.blit(DEFEAT_CAGE, DEFEAT_CAGE_RECT)
