''' ============================================================= '''
''' ========== HANDLING EVERYTHING IN THE MENU SCREEN =========== '''
''' ============================================================= '''

from assets import WASD_CONTROLS_A, WASD_RECT_A, ARROWS_CONTROLS_A, ARROWS_RECT_A

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class Menu(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.bobbing_interval = 30
        self.interval_toggle = False
        self.title_interval = 15
        self.title_index = 0
        self.title_anim = ['-']

        self.player_offset = [0, -100, 100]

    def set_title(self, game):
        self.title_anim = [
            f' - = -{game.title_name}- = - ',
            f'- - = {game.title_name} = - -',
            f' - - ={game.title_name}= - - ',
            f'- - - {game.title_name} - - -',
            f' - - -{game.title_name}- - - ',
            f'= - - {game.title_name} - - =',
            f' = - -{game.title_name}- - = ',
            f'- = - {game.title_name} - = -',
        ]

    def draw(self, game):
        game.screen.fill(colors.space_blue)

        if game.title_name == '< WESTERN RAID >':
            game.stars.update(game)
            self.bobbing_interval = 30
            self.title_interval = 15

            for player in [game.player_1, game.player_2]:
                if player:
                    player.set_eyes('base_eyes')
                    player.set_offset(None, [-4, 0])

        else:
            game.win_stars.update(game)
            self.bobbing_interval = 20
            self.title_interval = 5

            for player in [game.player_1, game.player_2]:
                if player:
                    player.set_eyes('happy_eyes')

        if game.tick % self.title_interval == 0:
            self.title_index += 1
            if self.title_index > len(self.title_anim) - 1:
                self.title_index = 0

        game.text.title_text.set_text(self.title_anim[self.title_index])
        game.text.title_text.draw(game)
        game.text.volume_text.draw(game)
        game.text.full_score_text.rect = (game.screen_width / 2, 180)
        game.text.full_score_text.string = str("TOTAL SCORE: {:08d}".format(game.data["total_score"]))
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

        game.players_animate(self.player_offset)

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

        if game.esc_pressed:
            game.text.quit_text.draw(game)
