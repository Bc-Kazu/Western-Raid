''' ============================================================= '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN ROUND ========== '''
''' ============================================================= '''

from assets import WASD_CONTROLS_B, ARROWS_CONTROLS_B
from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

import pygame as pg

class Round(GameScene):
    # Process for different types of scenes to play within the round
    INIT_CUTSCENE_PROCESS = {
        'name': 'init_cutscene',
        'initialize': False,
        'tick': 0,
        'fall_interval': 120,
        'fall_speed': 3,
        'broken_ufo': False,
        'destroy_interval': 180,
        'player_velocity': [(0, 0), (-8, -8), (8, -8)],
        'player_fall': [False, False, False],
        'multX': 0.97,
        'multY': 0.92,
        'shield_show': False,
        'timer': 0,
        'timer_interval': 300,
        'wait_interval': 360,
        'end_interval': 420,
        'finalize': False
    }

    STARTUP_PROCESS = {
        'name': 'startup',
        'initialize': True,
        'tick': 0,
        'text_blink_interval': 240,
        'controls_show': True,
        'control_blink_interval': 420,
        'end_interval': 500,
        'finalize': False
    }

    AMBUSH_PROCESS = {
        'name': 'ambush',
        'initialize': False,
        'tick': 0,
        'filter_show': True,
        'filter_interval': 60,
        'display_text': True,
        'end_interval': 360,
        'finalize': False
    }

    DEFEAT_PROCESS = {
        'name': 'defeat',
        'initialize': False,
        'tick': 0,
        'blink': False,
        'blink_interval': 120,
        'end_interval': 180,
        'finalize': False
    }

    REBUILD_PROCESS = {
        'name': 'rebuild',
        'initialize': False,
        'finalize': False
    }

    VICTORY_PROCESS = {
        'name': 'victory',
        'initialize': False,
        'players_inside': False,
        'tick': 0,
        'escape_interval': 380,
        'blink': False,
        'blink_interval': 460,
        'end_interval': 520,
        'finalize': False
    }

    BASE_STATE_DICT = {
        STARTUP_PROCESS['name']: STARTUP_PROCESS.copy(),
        AMBUSH_PROCESS['name']: AMBUSH_PROCESS.copy(),
        DEFEAT_PROCESS['name']: DEFEAT_PROCESS.copy(),
        REBUILD_PROCESS['name']: REBUILD_PROCESS.copy(),
        VICTORY_PROCESS['name']: VICTORY_PROCESS.copy(),
        INIT_CUTSCENE_PROCESS['name']: INIT_CUTSCENE_PROCESS.copy(),
    }

    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.ufo_goal_pos = None

    def _time_up_draw(self, game):
        # Drawing custom time up screen
        game.text.timer_text.current_color = (100, 255, 100)
        time_up_tick = 0
        game.sound.play('none')
        game.sound.play_sfx('time_up')

        while time_up_tick <= 25:
            time_up_tick += 1

            game.screen.fill(game.level.background_color)
            game.ufo.draw(game)
            for terrain in game.level.map:
                terrain.draw(game)

            game.text.timer_text.string = '00:00'
            if time_up_tick % 2 == 0: game.text.timer_text.draw(game)
            pg.display.flip()

            pg.time.delay(80)

        game.text.timer_text.current_color = (255, 255, 255)

    def _rebuild_draw(self, game):
        # Drawing custom UFO screen
        game.screen.fill(game.level.background_color)
        game.ufo.draw(game)
        for terrain in game.level.map:
            terrain.draw(game)

        if game.player_1:
            game.text.p1_points_text.string = str("{:05d}".format(game.player_1.score))
            game.text.p1_points_text.draw(game)
        if game.player_2:
            game.text.p2_points_text.string = str("{:05d}".format(game.player_2.score))
            game.text.p2_points_text.draw(game)
        pg.display.flip()

    def _rebuild_process(self, game):
        self._time_up_draw(game)

        # Recovering UFO gradually
        cooldown_factor = 0
        layers_built = 0

        for block in game.ufo.blocks:
            if block.strength > 0:
                cooldown_factor += block.strength
            else:
                cooldown_factor -= 1

        cooldown_factor = cooldown_factor / 20
        if cooldown_factor < 1: cooldown_factor = 1
        if cooldown_factor > 2: cooldown_factor = 2
        reward_ufo_colors = [
            colors.yellow,
            colors.bright_cyan,
            colors.hot_pink
        ]

        for layer in range(1, 4):
            blocks_built = 0
            max_blocks = 0

            for block in game.ufo.blocks:
                max_blocks += 1
                built = False

                if block.strength >= layer:
                    blocks_built += 1
                    built = True

                    if layer == 1:
                        if game.player_1: game.player_1.get_score(game, 50)
                        if game.player_2: game.player_2.get_score(game, 50)
                        game.sound.play_sfx('points')
                    else:
                        game.sound.play_sfx('points_extra')

                    block.set_color(reward_ufo_colors[layer - 1])

                elif block.strength == 0:
                    built = True
                    game.sound.play_sfx('brick_get')
                    block.set_strength(1)

                if built:
                    self._rebuild_draw(game)
                    pg.time.delay(int(100 // cooldown_factor))

            if blocks_built >= max_blocks:
                layers_built += 1
                pg.time.delay(100)
                game.sound.play_sfx('points')

                if layers_built >= 2:
                    game.sound.play_sfx('powerup_get')
                if layers_built >= 3:
                    game.sound.play_sfx('start')

                game.sound.play_sfx(f'reward{layers_built}')
                if game.player_1: game.player_1.get_score(game, 1000 * layers_built)
                if game.player_2: game.player_2.get_score(game, 1000 * layers_built)
            else:
                break

        self._rebuild_draw(game)
        pg.time.delay(1000)
        game.sound.play('you_should_probably_get_in_the_ufo_now', -1)
        game.sound.play_sfx('ufo_rebuild')
        self.set_state('victory')

    def _get_controls(self, player):
        if player:
            return WASD_CONTROLS_B if player.controls == 'WASD' else ARROWS_CONTROLS_B
        return None

    def _show_controls(self, game, specific=None):
        if not specific:
            # Displaying player controls if player exists
            for player in [game.player_1, game.player_2]:
                player_control = self._get_controls(player)
                if player and player_control:
                    rect = player.rect
                    game.screen.blit(player_control, (rect.x - 2, rect.y - 50))
        else:
            player_control = self._get_controls(specific)
            rect = specific.rect
            game.screen.blit(player_control, (rect.x - 2, rect.y - 50))

    def _init_cutscene(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.state['initialize'] = True
            self.ufo_goal_pos = game.ufo.rect.y
            game.ufo.set_position((game.ufo.rect.x, -game.ufo.size[1]))
            game.ufo.visible = True
            game.ufo.always_on_top = True

            for player in [game.player_1, game.player_2]:
                if player:
                    player.shield_visible = False
                    player.set_position((game.screen_width // 2, game.screen_height // 2), True)
        else:
            self.state['tick'] += 1

        if game.ufo.rect.y < self.ufo_goal_pos:
            if self.state['tick'] < self.state['fall_interval']:
                self.state['fall_speed'] *= 1.03
                game.ufo.set_position(game.ufo.rect.x, game.ufo.rect.y + self.state['fall_speed'])
        elif not self.state['broken_ufo']:
            game.ufo.set_position(game.ufo.rect.x, self.ufo_goal_pos)
            self.state['broken_ufo'] = True
            self.state['tick'] = self.state['fall_interval']
            game.ufo.set_blink(True, 5)

        if self.state['tick'] == self.state['destroy_interval']:
            game.ufo.set_blink(False)
            game.ufo.visible = False
            game.ufo.always_on_top = False

        if self.state['tick'] > self.state['destroy_interval']:
            for player in [game.player_1, game.player_2]:
                if not player:
                    continue

                velocity = self.state['player_velocity'][player.id]
                player.set_velocity(velocity)

                if player.id == 2:
                    player.set_offset(None, [4, 0])

                if velocity[1] > -1 and not self.state['player_fall'][player.id] :
                    self.state['player_fall'][player.id] = True
                    velocity = (velocity[0], 1)
                elif self.state['player_fall'][player.id]:
                    self.state['multY'] = 1.07
                else:
                    player.set_eyes('shock_eyes')

                if player.rect.y > 300 and self.state['player_fall'][player.id] :
                    player.set_position(player.rect.x, 300)
                    self.state['multY'] = 0
                    player.set_eyes('squint_eyes')

                if self.state['tick'] > self.state['timer_interval']:
                    player.set_eyes('base_eyes')
                    if self.state['tick'] % 10 == 0:
                        player.shield_visible = not player.shield_visible

                new_velocity = (velocity[0] * self.state['multX'], velocity[1] * self.state['multY'])
                self.state['player_velocity'][player.id] = new_velocity

        if self.state['tick'] > self.state['timer_interval']:
            self.state['timer'] += game.level.round_time // 60
            if self.state['timer'] > game.level.round_time:
                self.state['timer'] = game.level.round_time
            seconds = self.state['timer'] % 60
            minutes = int(self.state['timer'] / 60) % 60
            game.text.timer_text.set_text(f'{minutes:02}:{seconds:02}')
        if self.state['tick'] > self.state['wait_interval']:
            self.state['timer'] = game.level.round_time
            game.text.timer_text.set_blink(True, 5)

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            self.state['finalize'] = True
            game.text.timer_text.set_blink(False)
            game.level.start()

            for player in [game.player_1, game.player_2]:
                if player: player.shield_visible = True

            self.set_state('startup')

    def _startup_process(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.state['initialize'] = True
        else:
            self.state['tick'] += 1

        if game.level.index == 1:
            game.text.begin_message.draw(game)
            game.text.defend_message.draw(game)

        if self.state['controls_show']:
            self._show_controls(game)

        # Processing toggle of filter and text
        if self.state['tick'] > self.state['text_blink_interval']:
            game.text.begin_message.set_blink(True)
        if self.state['tick'] > self.state['control_blink_interval']:
            game.text.begin_message.toggle(False)
            game.text.defend_message.set_blink(True)
            if self.state['tick'] % 8 == 0:
                self.state['controls_show'] = not self.state['controls_show']

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            game.text.begin_message.toggle(True)
            game.text.begin_message.set_blink(False)
            game.text.defend_message.set_blink(False)
            self.state['finalize'] = True
            self.set_state()

    def _defeat_process(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.state['initialize'] = True
            game.sound.play('none')
            game.sound.play_sfx('ufo_destroy')

            game.ufo.set_blink(True)
            game.player_1.set_eyes('shock_eyes')
            if game.player_2:
                game.player_2.set_eyes('shock_eyes')
        else:
            self.state['tick'] += 1

        # Blinking the screen between round and defeat backgrounds
        if self.state['tick'] > self.state['blink_interval']:
            if self.state['tick'] % 8 == 0:
                self.state['blink'] = not self.state['blink']

                if self.state['blink']:
                    game.screen.fill(colors.sad_orange)
                else:
                    game.screen.fill(game.level.background_color)

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            self.state['finalize'] = True
            game.set_scene('defeat')
            game.sound.play('defeat')
            game.set_final_score('defeat')
            game.ufo.set_blink(False)

    def _victory_process(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.state['initialize'] = True

        # Waiting for players to get inside the UFO
        if not self.state['players_inside']:
            game.text.get_in.draw(game)
            self.state['players_inside'] = game.ufo.victory_check(game)
        else:
            # Start animation for escaping
            if self.state['tick'] == 0:
                game.sound.play('escape')

            self.state['tick'] += 1

            if self.state['tick'] < self.state['escape_interval']:
                game.ufo.victory_check(game)
            elif self.state['tick'] < self.state['blink_interval']:
                if self.state['tick'] % 8 == 0:
                    self.state['blink'] = not self.state['blink']

                    if self.state['blink']:
                        game.screen.fill(colors.space_purple)
                    else:
                        game.screen.fill(game.level.background_color)
            else:
                game.screen.fill(colors.black)

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            self.state['finalize'] = True
            game.sound.play('victory', -1)
            game.set_scene('victory')
            game.set_final_score('victory')

    def _ambush_process(self, game):
        # Initializing the process
        if not self.state['initialize']:
            self.state['initialize'] = True
            game.sound.play('BANDIT-RAID', -1)
            game.sound.play_sfx('ambush')
        else:
            self.state['tick'] += 1

        game.text.ambush_text.draw(game)

        # Processing toggle of filter and text
        if self.state['tick'] < self.state['filter_interval']:
            if self.state['tick'] % 5 == 0:
                self.state['filter_show'] = not self.state['filter_show']
        else:
            self.state['filter_show'] = True

        # Finalizing the process
        if self.state['tick'] > self.state['end_interval']:
            self.state['finalize'] = True
            self.set_state()

    def draw(self, game):
        game.screen.fill(game.level.background_color)
        if game.stars.enabled: game.stars.enabled = False

        # Temporary list for hazzards to be prioritized by their Y position
        draw_queue = []

        for terrain in game.level.map:
            terrain_Zindex = terrain.rect.y + int(terrain.size[1] / 2) if terrain.size[
                                                                              1] < 90 else terrain.rect.y + int(
                terrain.size[1] / 1.4)
            draw_queue.append((terrain_Zindex, terrain))

        if game.player_1:
            draw_queue.append((game.player_1.rect.centery, game.player_1))
        if game.player_2:
            draw_queue.append((game.player_2.rect.centery, game.player_2))

        draw_queue.extend((obj.rect.centery, obj) for obj in game.level.objects)
        draw_queue.extend((gadget.rect.centery, gadget) for gadget in game.level.gadgets)
        draw_queue.extend((bandit.rect.centery, bandit) for bandit in game.level.bandits)
        draw_queue.extend((bullet.rect.centery, bullet) for bullet in game.level.bullets)

        if not game.ufo.always_on_top:
            draw_queue.append((game.ufo.rect.centery + game.ufo.size[1] / 3.5, game.ufo))

        # This function sorts all hazzards by their Y position, to handle the Z-Index effect
        draw_queue.sort(key=lambda obj: obj[0])  # O(n log n) <- function used in sorting

        for _, obj in draw_queue:
            obj.draw(game)

        if game.player_1:
            if game.player_1.stuck:
                self._show_controls(game, game.player_1)

            game.text.p1_points_text.string = str("{:05d}".format(game.player_1.score))
            game.text.p1_points_text.rect = (90, 30)
            game.text.p1_points_text.draw(game)

        if game.player_2:
            if game.player_1.stuck:
                self._show_controls(game, game.player_2)

            game.text.p2_points_text.string = str("{:05d}".format(game.player_2.score))
            game.text.p2_points_text.rect = (game.screen_width - 90, 30)
            game.text.p2_points_text.draw(game)

        if game.ufo.always_on_top:
            game.ufo.draw(game)

        for message in game.level.message_popups:
            message.draw(game)

        if not self.state or self.state['name'] != 'init_cutscene':
            time_left = game.level.round_time - game.level.time_elapsed
            seconds = time_left % 60
            minutes = int(time_left / 60) % 60
            game.text.timer_text.set_text(f'{minutes:02}:{seconds:02}')

        if self._state_check('startup'):
            self._startup_process(game)

        if game.debug:
            if game.player_1:
                game.screen.blit(game.player_1.hitbox_area, game.player_1.hitbox)
            if game.player_2:
                game.screen.blit(game.player_2.hitbox_area, game.player_2.hitbox)

        if not self.state or not self.state['name'] == 'victory':
            game.text.timer_text.draw(game)

        if game.esc_pressed:
            game.text.escape_text.draw(game)

        # Conditions for different states
        if self._state_check('defeat'):
            self._defeat_process(game)
        if self._state_check('rebuild'):
            self._rebuild_process(game)
        if self._state_check('victory'):
            self._victory_process(game)
        if self._state_check('init_cutscene'):
            self._init_cutscene(game)

        # Conditions for ambush mode visuals
        if self._state_check('ambush'):
            self._ambush_process(game)
            if self.state and self.state.get('filter_show', False):
                game.screen.blit(game.ambush_filter, (0, 0))

        if game.level.ambush_mode and not self.state:
            game.screen.blit(game.ambush_filter, (0, 0))