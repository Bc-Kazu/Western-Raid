''' ===================================================================== '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN LEVEL SELECT  ========== '''
''' ===================================================================== '''

from assets import UFO_SPRITE_RECT, UFO_SPRITE_RECT2, UFO_SPRITE, UFO_SPRITE2, LEVEL_FRAMES, LEVEL_ICONS, \
    LEVEL_FRAMES_RECT, LEVEL_ICONS_RECT, LEVEL_LOCKS, LEVEL_LOCKS_RECT

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class LevelSelect(GameScene):
    START_PROCESS = {
        'name': 'start',
        'initialize': False,
        'tick': 0,
        'fall_interval': 60,
        'fall_offset': [0, 0, 0],
        'end_interval': 220,
        'finalize': False,
    }

    BASE_STATE_DICT = {
        START_PROCESS['name']: START_PROCESS.copy()
    }

    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.bobbing_interval = 30
        self.shake_interval = 6
        self.eyes_interval = 8

        self.level_selected = None
        self.selected_blink = False
        self.player_offset = [0, -100, 100]
        self.player_shake = 12
        self.fall_speed = 1

        self.fall_index = [0, 0, 1]
        self.fall_offset_list = [
            (0, -6),
            (-2, -2),
            (-4, -6),
            (-2, -2),
        ]

        self.ufo_dict = {1: [UFO_SPRITE, UFO_SPRITE_RECT], 2: [UFO_SPRITE2, UFO_SPRITE_RECT2]}

    def _start_process(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.level_selected = game.base_level
            self.player_offset = [0, -100, 100]
            self.player_shake = 12
            self.fall_speed = 2

            game.sound.play('none')
            game.sound.play_sfx('start')
            game.sound.play_sfx('ufo_break')

            lv_name = getattr(game.text, f"level{self.level_selected}_select")
            lv_name.set_color_blink(True, 8, colors.green, colors.white)

            self.state['initialize'] = True
        else:
            self.state['tick'] += 1

        if self.state['tick'] < self.state['fall_interval']:
            if self.state['tick'] % self.shake_interval == 0:
                self.player_shake /= 1.2
                self.player_shake = -self.player_shake
        elif self.state['tick'] == self.state['fall_interval']:
            game.sound.play_sfx('fall_menu')

        for player in [game.player_1, game.player_2]:
            if not player:
                continue

            if self.state['tick'] % self.eyes_interval == 0:
                self.fall_index[player.id] += 1
                if self.fall_index[player.id] > len(self.fall_offset_list) - 1:
                    self.fall_index[player.id] = 0

                if self.state['tick'] < self.state['fall_interval'] - 20:
                    shocked = player.current_eyes == player.eyes_dict['shock_eyes']
                    player.set_eyes('closed_eyes' if shocked else 'shock_eyes')
                else:
                    player.set_eyes('shock_eyes')

            new_x = game.screen_width // 2 + self.player_offset[player.id]
            new_y = game.player_menu_y
            player.set_offset(None, [-4, 0])
            falling = self.state['tick'] >= self.state['fall_interval']

            if not falling:
                new_x += self.player_shake
                player.set_offset(None, [-3, 0])
                self.state['fall_offset'][player.id] -= self.fall_speed / 3
            elif self.state['tick'] < self.state['end_interval']:
                offset = self.fall_offset_list[self.fall_index[player.id]]
                player.set_offset(None, offset)
                self.fall_speed *= 1.02
                self.state['fall_offset'][player.id] += self.fall_speed
                player.set_eyes('squint_eyes')
            else:
                player.set_eyes('base_eyes')

            new_y += self.state['fall_offset'][player.id]
            player.set_position(new_x, new_y, True)
            player.draw(game)

            ufo = self.ufo_dict[player.id]
            ufo[1].centerx = new_x
            ufo[1].centery = new_y - (20 if not falling else 16)
            game.screen.blit(ufo[0], ufo[1])

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            self.state['finalize'] = True
            self.set_state()
            game.enter_level()

            lv_name = getattr(game.text, f"level{self.level_selected}_select")
            lv_name.set_color_blink(False)

    def draw(self, game):
        game.screen.fill(colors.space_blue)
        game.stars.update(game)
        self.tick += 1

        for i in range(len(LEVEL_FRAMES)):
            if not self.level_selected:
                getattr(game.text, f"level{i + 1}_select").set_color(colors.grey)
            LEVEL_FRAMES[i].set_alpha(100)
            LEVEL_ICONS[i].set_alpha(100)

        # Set active level to highlighted state
        if game.base_level in game.allowed_levels:
            if not self.level_selected:
                level_names = [
                    'LOCKED',
                    'DESERT',
                    'SALOON',
                    'BARREN',
                    'CARTEL',
                    '???']

                i = game.base_level
                unlocked = game.data[f'level{i}']['unlocked']
                lv_name = f'---< [ {level_names[i] if unlocked else level_names[0]} ] >---'
                best_text = 'BEST SCORE: ' + str(game.data[f'level{i}']['best_score'])
                getattr(game.text, f"level{i}_select").set_color(colors.white)
                getattr(game.text, f"level{i}_name").set_text(lv_name)
                getattr(game.text, f"level{i}_best").set_text(best_text)
                getattr(game.text, f"level{i}_name").draw(game)
                getattr(game.text, f"level{i}_best").draw(game)

            LEVEL_FRAMES[game.base_level - 1].set_alpha(255)
            LEVEL_ICONS[game.base_level - 1].set_alpha(255)


        for i in range(1, 6):
            getattr(game.text, f"level{i}_select").draw(game)

        if not self.level_selected:
            game.text.level_select.draw(game)
            game.text.select_tip.draw(game)

            if game.tick % self.bobbing_interval == 0:
                game.player_bobbing = -game.player_bobbing
        else:
            lv = self.level_selected - 1

            if self.tick % 8 == 0:
                self.selected_blink = not self.selected_blink

            alpha = 0 if self.selected_blink else 255
            alpha2 = 128 if self.selected_blink else 255

            LEVEL_FRAMES[lv].set_alpha(alpha)
            LEVEL_ICONS[lv].set_alpha(alpha2)

        # Draw level frames, icons, and locks if locked
        for i in range(len(LEVEL_FRAMES)):
            game.screen.blit(LEVEL_FRAMES[i], LEVEL_FRAMES_RECT[i])
            game.screen.blit(LEVEL_ICONS[i], LEVEL_ICONS_RECT[i])

            if not game.data[f"level{i + 1}"]["unlocked"]:
                game.screen.blit(LEVEL_LOCKS[i], LEVEL_LOCKS_RECT[i])

        if self._state_check('start'):
            self._start_process(game)
        else:
            game.players_animate(self.ufo_dict, self.player_offset)