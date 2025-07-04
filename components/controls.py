"""
Module that handles all input interactions with the game
"""
from assets import WASD_RECT_A, ARROWS_RECT_A, LEVEL_FRAMES, LEVEL_FRAMES_RECT, MYSTERIOUS_RECT
from utils.colors import Colors
colors = Colors()

import pygame as pg

def input_once(game, given_keys, AND_MODE=False):
    if not AND_MODE:
        for key in given_keys if isinstance(given_keys, list) else [given_keys]:
            if key in game.keys_pressed_once and game.key_ui_pressed:
                game.key_ui_pressed = False
                return True

        return False
    else:
        pressed = True

        for key in given_keys if isinstance(given_keys, list) else [given_keys]:
            if game.keys_pressed[key] and game.key_ui_pressed:
                continue
            else:
                pressed = False

        game.key_ui_pressed = not pressed
        return pressed


def handle_events(game):
    keys = pg.key.get_pressed()
    game.keys_pressed = keys
    game.keys_pressed_once = []
    mouse_states = {'left': 1, 'scroll': 2, 'right': 3}
    mouse_input = 0
    mouse_wheel = None

    # ========== Getting the events and inputs ========== #
    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            game.running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_input = event.button
        if event.type == pg.MOUSEWHEEL:
            mouse_wheel = event

        if event.type == pg.KEYDOWN:
            game.key_ui_pressed = True
            game.keys_pressed_once.append(event.key)
        elif event.type == pg.KEYUP:
            game.key_ui_pressed = False

            if event.key == pg.K_ESCAPE:
                game.escape_tick = 0
                game.text.escape_text.set_color()
                game.text.quit_text.set_color()

            if event.key == pg.K_RETURN:
                game.return_tick = 0
                game.text.data_reset_accept.set_color()

    # ========== UI Mouse interactions ========== #
    mouse_pos = pg.mouse.get_pos()

    if game.scene.name == 'menu':
        if mouse_input == mouse_states['left']:
            for player in [game.player_1, game.player_2]:
                if player and game.ufo_skins[player.id].rect.collidepoint(mouse_pos):
                    game.set_scene('level_select')
                    game.sound.play_sfx('ui_select')

            if WASD_RECT_A.collidepoint(mouse_pos):
                game.add_player('WASD')
            if ARROWS_RECT_A.collidepoint(mouse_pos):
                game.add_player('ARROWS')
            if MYSTERIOUS_RECT.collidepoint(mouse_pos):
                game.text.mysterious_text.toggle(True)
                game.sound.play_sfx('player_shoot')

        elif mouse_input == mouse_states['right']:
            for player in [game.player_1, game.player_2]:
                if player and game.ufo_skins[player.id].rect.collidepoint(mouse_pos):
                    game.player_1 = None if player.id == 1 else game.player_1
                    game.player_2 = None
                    game.player_count = 2 - player.id
                    game.sound.play_sfx('remove')

            for particle in game.stars.particles:
                if particle.rect.collidepoint(mouse_pos):
                    particle.color = colors.window_light_yellow
                    game.sound.play_sfx('block_break_extra')

    if mouse_input == 1 and game.scene.name == 'level_select':
        for level in LEVEL_FRAMES.keys():
            if LEVEL_FRAMES_RECT[level].collidepoint(mouse_pos):
                game.set_level(level, True)

    # ========== Player joining inputs ========== #
    if game.scene.name == 'menu' or game.scene.name == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            game.add_player('WASD')
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            game.add_player('ARROWS')

    # ========== Scene scrolling inputs ========== #
    if game.scene.name == 'menu' and game.scene.on_credits:
        max_top = game.scene.ui_offset[1] < game.scene.credits_offset[1]
        max_bottom = game.scene.ui_offset[1] > game.scene.credits_offset[1] * 2
        if (keys[pg.K_w] or keys[pg.K_UP]) and max_top:
            game.scene.set_offset([0, game.scene.ui_offset[1] + 2])
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and max_bottom:
            game.scene.set_offset([0, game.scene.ui_offset[1] - 2])

        if mouse_wheel and mouse_wheel.y < 0 and max_bottom:
            game.scene.set_offset([0, game.scene.ui_offset[1] + mouse_wheel.y * 15])
        if mouse_wheel and mouse_wheel.y > 0 and max_top:
            game.scene.set_offset([0, game.scene.ui_offset[1] + mouse_wheel.y * 15])

    # ========== level selection inputs ========== #
    if game.scene.name == 'level_select' and not game.scene.state:
        if input_once(game, [pg.K_RIGHT, pg.K_d]):
            game.set_level(game.base_level + 1)
        if input_once(game, [pg.K_LEFT, pg.K_a]):
            game.set_level(game.base_level - 1)

    if input_once(game, pg.K_RETURN):
        if game.scene.name == 'menu':
            if not game.scene.state:
                if game.player_1:
                    game.set_scene('level_select')
                    game.sound.play_sfx('ui_select')
                    return
                else:
                    # Refuse joining if no players selected
                    game.text.choose_text.toggle(True)
                    game.text.choose_text.set_color_blink(True)
                    game.set_hud(game.text.choose_text)
                    game.sound.play_sfx('push')

        # Starting level if possible
        if game.scene.name == 'level_select' and game.player_1:
            game.enter_level()
        if game.scene.name == 'victory' or game.scene.name == 'defeat':
            game.sound.play_sfx('ui_select')
            game.game_reset()

    if keys[pg.K_RETURN]:
        if game.scene.state and game.scene.state['name'] == 'data_reset':
            if game.return_tick > game.return_interval:
                game.return_tick = 0
                game.data_reset()
                game.scene.set_state()
            else:
                game.return_tick += 1
                game.text.data_reset_accept.set_color(
                    (max(0, 255 - game.return_tick * 3), 255,
                     max(0, 255 - game.return_tick * 3)))

    # Removing players by keyboard
    if input_once(game, pg.K_BACKSPACE):
        if game.scene.name == 'menu':
            if not game.scene.state and (game.player_1 or game.player_2):
                game.sound.play_sfx('remove')
                game.player_1 = None
                game.player_2 = None

    # Toggling credits
    if input_once(game, pg.K_c) and game.scene.name == 'menu':
        game.scene.set_credits(not game.scene.on_credits)

    # Input for super cool menu background and music
    if input_once(game, pg.K_r):
        if game.scene.name == 'menu' and game.data['level1']['wins'] > 0:
            if game.title_name == '< WESTERN RAID >':
                game.set_title('< WESTERN RAVE >')
                game.scene.set_title(game)
                game.set_music('martian_rave')
            else:
                game.set_title()
                game.scene.set_title(game)
                game.set_music('menu')

    # ========== Cat mode inputs (meow :3) ========== #
    if input_once(game, pg.K_k) and game.scene.name == 'menu' and game.player_1:
        if game.block_skin == 'happy_cat':
            game.set_skin()
            game.set_block()
            game.sound.play_sfx('ui_select')
            game.sound.play_sfx('swap')
            game.text.muted.set_text(f'CAT NO :(')
            game.set_hud(game.text.muted)
        else:
            game.set_skin('cat_ufo')
            game.set_block('happy_cat', 'sad_cat')
            game.sound.play_sfx('ui_select')
            game.sound.play_sfx('meow')
            game.text.muted.set_text(f'CAT YES :)')
            game.set_hud(game.text.muted)

    # Some weird effect I added that I forgot the use of
    if input_once(game, pg.K_F7):
        if game.player_1 is not None:
            game.player_1.set_super()
    if input_once(game, pg.K_F8):
        if game.player_2 is not None:
            game.player_2.set_super()

    # ========== Data Reset inputs ========== #
    if input_once(game, [pg.K_LSHIFT, pg.K_BACKSPACE], True):
        if game.scene.name == 'menu' and not game.scene.state:
            game.scene.set_state('data_reset')


    # Checking for quitting scene or game
    if keys[pg.K_ESCAPE]:
        game.esc_pressed = True

        if game.scene.name == 'menu':
            if game.escape_tick > game.escape_interval:
                game.running = False
            else:
                game.escape_tick += 1
                game.text.quit_text.set_alpha(game.escape_tick * 3)

            if game.scene.state and game.scene.state['name'] == 'data_reset':
                game.scene.reset_state('data_reset')
                game.scene.set_state()

        if game.scene.name == 'level_select' and not game.scene.state:
            game.sound.play_sfx('ui_select')
            game.set_scene('menu')

        if game.scene.name == 'round':
            if game.escape_tick > game.escape_interval:
                game.escape_tick = 0
                game.set_scene('menu')
                game.game_reset()
            else:
                game.escape_tick += 1
                game.text.escape_text.set_alpha(game.escape_tick * 3)
    else:
        game.esc_pressed = False

    if input_once(game, pg.K_F3):
        if game.debug: game.text.debug.set_text(f'DEBUG [ OFF ]')
        else: game.text.debug.set_text(f'DEBUG [ ON ]')
        game.set_hud(game.text.debug)
        game.debug = not game.debug
    elif input_once(game, pg.K_0):
        if game.sound.mute: game.text.muted.set_text(f'MUTE [ DISABLED ]')
        else: game.text.muted.set_text(f'MUTE [ ENABLED ]')
        game.set_hud(game.text.muted)
        game.sound.mute_music()
    elif input_once(game, pg.K_EQUALS) or input_once(game, pg.K_PLUS):
        game.sound.change_volume('increase')
        game.text.music_change_vol.set_text(f'+ Music: {int(10 * game.sound.music_offset)}')
        game.set_hud(game.text.music_change_vol)
    elif input_once(game, pg.K_MINUS):
        game.sound.change_volume('decrease')
        game.text.music_change_vol.set_text(f'- Music: {int(10 * game.sound.music_offset)}')
        game.set_hud(game.text.music_change_vol)
    elif input_once(game, pg.K_RIGHTBRACKET) or input_once(game, pg.K_RIGHTPAREN):
        game.sound.change_volume_sfx('increase')
        game.text.sfx_change_vol.set_text(f'+ SFX: {int(10 * game.sound.sfx_offset)}')
        game.set_hud(game.text.sfx_change_vol)
    elif input_once(game, pg.K_LEFTBRACKET) or input_once(game, pg.K_LEFTPAREN):
        game.sound.change_volume_sfx('decrease')
        game.text.sfx_change_vol.set_text(f'- SFX: {int(10 * game.sound.sfx_offset)}')
        game.set_hud(game.text.sfx_change_vol)