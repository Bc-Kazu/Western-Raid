''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE VICTORY SCREEN ========= '''
''' ============================================================= '''

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class Victory(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.bobbing_interval = 20
        self.player_offset = [0, 100, 300]
        self.score_rects = [(0, 0), (195, 300), (200, 350)]

    def draw(self, game):
        if not self.initialize:

            for player in [game.player_1, game.player_2]:
                if player:
                    game.ufo_skins[player.id].rect.center = (game.screen_width / 2, 420)

                    player.set_position((game.screen_width / 2, 440), True)
                    player.set_eyes('happy_eyes')
                    player.facing_up = False

            self.initialize = True

        game.screen.fill(colors.space_purple)
        game.win_stars.update(game)

        game.text.survived_text.draw(game)
        game.text.final_message.draw(game)

        final_score = game.player_1.score + (game.player_2.score if game.player_2 else 0)

        game.text.full_score_text.set_position(265, 250)
        game.text.full_score_text.set_text("FINAL SCORE: {:06d}".format(final_score))
        game.text.full_score_text.draw(game)
        game.text.return_text.draw(game)

        text_list = [None, game.text.p1_points_text, game.text.p1_points_text]

        # Draw players
        if game.tick % self.bobbing_interval == 0:
            game.player_bobbing = -game.player_bobbing

        # Draw victory stats and players
        game.players_animate(self.player_offset)

        for player in [game.player_1, game.player_2]:
            if not player:
                continue

            text_list[player.id].set_text("PLAYER {:d}: {:06d}".format(player.id, player.score))
            text_list[player.id].set_position(self.score_rects[player.id])
            text_list[player.id].draw(game)