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

        final_score = game.player_1.score + (game.player_2.score if game.player_2 else 0)
        game.text.full_score_text.set_position(265, 250)
        game.text.full_score_text.string = str("FINAL SCORE: {:06d}".format(final_score))
        game.text.full_score_text.draw(game)
        game.text.return_text.draw(game)

        # Draw defeat stats and players
        for player in [game.player_1, game.player_2]:
            player.draw(game) if player else None

        game.screen.blit(DEFEAT_CAGE, DEFEAT_CAGE_RECT)
