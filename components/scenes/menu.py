''' ============================================================= '''
''' ========== HANDLING EVERYTHING IN THE MENU SCREEN =========== '''
''' ============================================================= '''

from assets import TITLE_SPRITE_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, \
    TITLE_SPRITE, UFO_SPRITE, TITLE_SPRITE2, UFO_SPRITE2, \
    TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT, TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2, WASD_CONTROLS_A, \
    WASD_RECT_A, ARROWS_CONTROLS_A, ARROWS_RECT_A

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class Menu(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.bobbing_interval = 30
        self.interval_toggle = False

        self.player_offset = [0, -100, 100]

        self.sprites_dict = {
            1: [[TITLE_SPRITE, TITLE_SPRITE_RECT], [TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT],
                      [UFO_SPRITE, UFO_SPRITE_RECT]],
            2: [[TITLE_SPRITE2, TITLE_SPRITE_RECT2], [TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2],
                      [UFO_SPRITE2, UFO_SPRITE_RECT2]]
        }

    def draw(self, game):
        game.screen.fill(colors.space_blue)
        game.stars.update(game)

        game.text.title_text.draw(game)
        game.text.volume_text.draw(game)
        game.text.full_score_text.rect = (game.screen_width / 2, 180)
        game.text.full_score_text.string = str("TOTAL SCORE: {:07d}".format(game.data["total_score"]))
        game.text.full_score_text.draw(game)
        game.text.new_best_text.draw(game)

        if game.tick % self.bobbing_interval == 0:
            self.interval_toggle = not self.interval_toggle

        if self.interval_toggle:
            WASD_CONTROLS_A.set_alpha(150)
            ARROWS_CONTROLS_A.set_alpha(150)
        else:
            WASD_CONTROLS_A.set_alpha(255)
            ARROWS_CONTROLS_A.set_alpha(255)

        # Draw players
        if game.tick % self.bobbing_interval == 0:
            game.player_bobbing = -game.player_bobbing

        for player in [game.player_1, game.player_2]:
            if not player:
                continue

            for sprite in self.sprites_dict[player.id]:
                sprite[1].centerx = game.screen_width // 2 + self.player_offset[player.id]
                sprite[1].centery = game.player_menu_y
                if sprite == self.sprites_dict[player.id][2]:
                    sprite[1].y -= 20

                if player.id % 2 == 0:
                    sprite[1].y -= game.player_bobbing
                else:
                    sprite[1].y += game.player_bobbing

                if sprite == self.sprites_dict[player.id][1]:
                    sprite[1].centerx -= 4

                game.screen.blit(sprite[0], sprite[1])

        # Draw texts and controls on screen depending on players joined
        if game.player_1:
            game.text.start_text.draw(game)
            game.text.choose_text.set_color_blink(False)
            game.text.choose_text.toggle(False)

            game.text.player1_text.set_position(game.screen_width / 2 + self.player_offset[1], 360)
            game.text.player2_text.draw(game)
        else:
            game.text.player1_text.set_position(game.screen_width / 2, 360)
            game.text.select_text.draw(game)
            WASD_RECT_A.center = (game.screen_width / 2 + self.player_offset[1], 460)
            game.screen.blit(WASD_CONTROLS_A, WASD_RECT_A)

        game.text.player1_text.draw(game)

        if not game.player_2:
            if game.player_1 and game.player_1.controls != 'WASD':
                WASD_RECT_A.center = (game.screen_width / 2 + self.player_offset[2], 460)
                game.screen.blit(WASD_CONTROLS_A, WASD_RECT_A)
            else:
                ARROWS_RECT_A.center = (game.screen_width / 2 + self.player_offset[2], 460)
                game.screen.blit(ARROWS_CONTROLS_A, ARROWS_RECT_A)
