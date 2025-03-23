"""
Class made to handle managing text and applying effects or changes
"""
from assets import TITLE_FONT, NORMAL_FONT, TEXT_FONT, SMALL_FONT
from utils.text import Text
from utils.colors import Colors
colors = Colors()

# Class create to store every preloaded text inside the game,
# along with its initial configurations
class TextStorage:
    def __init__(self, game):
        # ===============================================================
        # Creating MENU text/messages
        self.title_text = Text('< WESTERN RAID >', (game.screen_width / 2, 100), TITLE_FONT)
        self.player1_text = Text('PLAYER 1 :', (game.screen_width / 2 - 100, 360), TEXT_FONT, (180, 255, 180))
        self.player2_text = Text('PLAYER 2 :', (game.screen_width / 2 + 100, 360), TEXT_FONT, (255, 180, 255))
        self.select_text = Text('- CHOOSE PLAYER CONTROLS -',(game.screen_width / 2, 270), TEXT_FONT)
        self.controls_text = Text('0 = Mute     - & + keys = Change Music     '
                                '[ & ] keys = Change SFX     Backspace = Remove Players',
                              (game.screen_width / 2, 600), SMALL_FONT, (200, 200, 200))
        self.start_text = Text('< PRESS ENTER TO START >',(game.screen_width / 2, 270), TEXT_FONT)
        self.full_score_text = Text('TOTAL SCORE: 0000000', (game.screen_width / 2, 180), NORMAL_FONT)
        self.new_best_text = Text('NEW BEST!', (game.screen_width / 2, 220), TEXT_FONT)

        self.choose_text = Text('use WASD or ARROW keys to select your player',
                                (game.screen_width / 2, 540), TEXT_FONT, (220, 150, 50))
        self.mysterious_text = Text('[ He cannot talk, but is very clearly lost ]',
                 (200, 800), SMALL_FONT, colors.mid_light)
        self.mysterious_text.toggle(False)

        self.menu_list = [
            self.title_text, self.player1_text, self.player2_text, self.select_text,
            self.controls_text, self.start_text, self.full_score_text, self.new_best_text,
            self.choose_text]
        MID = game.screen_width // 2.4
        self.credits_list = [
            Text('> press C for credits <', (MID, -150), TEXT_FONT, colors.grey),
            Text('-- CREDITS --', (MID, -50), NORMAL_FONT),
            Text('CREATOR - BcDev (Paulo)', (MID, 0), TEXT_FONT),
            Text('INSPIRED BY - Breakout! (1976)', (MID, 80), TEXT_FONT),
            Text('ORIGINATED FROM - UEA Est, College Project', (MID, 120), TEXT_FONT),
            Text('= SPECIAL THANKS =', (MID, 190), TEXT_FONT, colors.pastel_purple),
            Text('My Teams and colleagues - Awesome people', (MID, 230), SMALL_FONT, colors.pastel_purple),
            Text('DaFluffyPotato - Awesome youtuber', (MID, 260), SMALL_FONT, colors.pastel_purple),
            Text('SFG Middlent - Awesome tips', (MID, 290), SMALL_FONT, colors.pastel_purple),
            Text('Dogs - Awesome animals', (MID, 320), SMALL_FONT, colors.pastel_purple),
            Text('Cats - Awesome too I guess...', (MID, 350), SMALL_FONT, colors.pastel_purple),
        ]

        # MENU text configurations
        self.new_best_text.toggle(False)
        self.new_best_text.set_color_blink(True, 10, (150, 255, 100))
        self.start_text.set_blink(True, 30)

        self.select_text.set_blink(True, 30)
        self.new_best_text.color_blink = True

        self.choose_text.set_color_blink(False, 8, (200, 100, 0))
        self.choose_text.toggle(False)

        # Data reset text
        self.data_reset = Text('RESET YOUR DATA?',(game.screen_width / 2, 180), TITLE_FONT)
        self.data_reset_warn = Text('Warning: This will rest all of your progress',
                                    (game.screen_width / 2, 250), TEXT_FONT, colors.red)

        self.data_reset_accept = Text('< ENTER - RESET >',(game.screen_width / 2, 300), TEXT_FONT)
        self.data_reset_decline = Text('< ESC - DECLINE >',(game.screen_width / 2, 350), TEXT_FONT)


        # ===============================================================
        # Creating LEVEL SELECT text/messages
        self.level_select = Text('= SELECT A LEVEL =', (game.screen_width / 2, 60), NORMAL_FONT)
        self.select_tip = Text('use A / D  or  LEFT / RIGHT',
                              (game.screen_width / 2, 100), TEXT_FONT, (120, 200, 255))

        for level in range(1, 6):
            offset = 164
            setattr(self, f'level{level}_name',
                    Text(f'XXXXXX:',(game.screen_width // 2, 300), NORMAL_FONT, colors.white))
            setattr(self, f'level{level}_best',
                    Text(f'BEST:',(game.screen_width // 2, 340), TEXT_FONT, colors.white))
            setattr(self, f'level{level}_index',
                    Text(f'LEVEL {level}:', (150 + (offset * (level - 1)), 150),
                         TEXT_FONT, colors.grey if level <= 3 else (100, 0, 0)))

        self.selected_level = Text('^ ^ ^',(150, 500), NORMAL_FONT)

        # LEVEL SELECT text configurations
        self.level_select.set_color_blink(True, 25, (180, 200, 255))

        # ===============================================================
        # Creating IN-ROUND text/messages
        self.p1_points_text = Text('00000', (90, 30), NORMAL_FONT)
        self.p2_points_text = Text('00000', (game.screen_width - 90, 30), NORMAL_FONT)
        self.timer_text = Text('00:00', (game.screen_width / 2, 30), NORMAL_FONT)
        self.defend_message = Text('Use your SHIELD to protect the UFO!',(game.screen_width / 2, 430), TEXT_FONT)
        self.begin_message = Text("!  Bandits will Attack  !",
                                (game.screen_width / 2, 170), TEXT_FONT, (255, 255, 0))
        self.ambush_text = Text('!! AMBUSH INCOMING !!', (game.screen_width / 2, 80), TEXT_FONT)
        self.get_in = Text('- THE SPACESHIP HAS BEEN FIXED! GET IN!! -', (game.screen_width / 2, 80), TEXT_FONT)

        # IN-ROUND text configurations
        self.timer_text.set_color_blink(False, 30, (0, 255, 0))
        self.defend_message.set_blink(False, 10)
        self.begin_message.set_blink(False, 10)
        self.ambush_text.set_color(colors.red)
        self.ambush_text.set_blink(True, 15)
        self.get_in.set_blink(True, 15)

        # ===============================================================
        # Creating LOADING text/messages
        self.loading = Text('Loading...', (game.screen_width / 2, game.screen_height / 2), NORMAL_FONT)
        self.loading_tip = Text("This is a tip! Wait, no its not.",
                                  (game.screen_width / 2, game.screen_height // 1.05), TEXT_FONT, (120, 200, 255))


        # ===============================================================
        # Creating VICTORY/DEFEAT text/messages
        self.survived_text = Text('-=[ YOU SURVIVED ]=-', (game.screen_width / 2, 100), TITLE_FONT)
        self.lost_text = Text('~X CAPTURED X~', (game.screen_width / 2, 100), TITLE_FONT,
                            (255, 160, 50))
        self.final_message = Text('CONGRATULATIONS!', (190, game.screen_height - 150),
                                TEXT_FONT, colors.white)
        self.return_text = Text('PRESS ENTER TO GO BACK TO MENU',
                              (game.screen_width / 2, game.screen_height - 40), TEXT_FONT)

        self.survived_text.set_color_blink(True, 30, (120, 255, 160))
        self.return_text.set_blink(True, 30)

        # ===============================================================
        # Creating UI text/messages
        self.debug = Text('DEBUG [ON]', (game.screen_width / 2, 15), SMALL_FONT, colors.white)
        self.music_change_vol = Text('> Music: 5', (game.screen_width / 2, 15), SMALL_FONT, colors.white)
        self.sfx_change_vol = Text('> SFX: 5', (game.screen_width / 2, 15), SMALL_FONT, colors.white)
        self.muted = Text('MUTE [ENABLED]', (game.screen_width / 2, 15), SMALL_FONT, colors.white)
        self.escape_text = Text('<  RETURNING TO MENU...  >', (game.screen_width / 2, game.screen_height - 100),
                               TEXT_FONT, colors.transparent)
        self.quit_text = Text('QUITTING...', (80, 20), TEXT_FONT, colors.transparent)

        # UI text configurations
        self.HUD_text_list = [None, 0, 180, False]
        self.debug.set_background(True)
        self.music_change_vol.set_background(True)
        self.sfx_change_vol.set_background(True)
        self.muted.set_background(True)