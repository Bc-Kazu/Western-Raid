"""
Module that handles all input interactions with the game
"""
from assets import WASD_RECT_A, ARROWS_RECT_A, LEVEL_FRAMES, LEVEL_FRAMES_RECT
from utils.colors import Colors
colors = Colors()

import pygame as pg

def input_once(game, key):
    if game.keys_pressed[key] and not game.key_ui_pressed:
        game.key_ui_pressed = True
        return True
    else:
        return False

def handle_events(game):
    keys = pg.key.get_pressed()
    game.keys_pressed = keys
    mouse_states = {'left': 1, 'scroll': 2, 'right': 3}
    mouse_input = 0

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            game.running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_input = event.button

        if event.type == pg.KEYDOWN:
            game.key_ui_pressed = True
        elif event.type == pg.KEYUP:
            game.key_ui_pressed = False

            if event.key == pg.K_ESCAPE:
                game.escape_tick = 0
                game.text.escape_text.set_color()
                game.text.quit_text.set_color()


    # ========== UI Button interactions ========== #
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
        elif mouse_input == mouse_states['right']:
            for player in [game.player_1, game.player_2]:
                if player and game.ufo_skins[player.id].rect.collidepoint(mouse_pos):
                    game.player_1 = None if player.id == 1 else game.player_1
                    game.player_2 = None
                    game.player_count = 2 - player.id
                    game.sound.play_sfx('remove')

    if mouse_input == 1 and game.scene.name == 'level_select':
        for level in LEVEL_FRAMES.keys():
            rect = LEVEL_FRAMES[level].get_rect()
            rect.topleft = LEVEL_FRAMES_RECT[level]

            if rect.collidepoint(mouse_pos):
                game.set_level(level, True)

    # Detecting player joining the components
    if game.scene.name == 'menu' or game.scene.name == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            game.add_player('WASD')
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            game.add_player('ARROWS')

    if game.scene.name == 'level_select' and not game.scene.state:
        if input_once(game, pg.K_RIGHT) or input_once(game, pg.K_d):
            game.set_level(game.base_level + 1)
        if input_once(game, pg.K_LEFT) or input_once(game, pg.K_a):
            game.set_level(game.base_level - 1)

    if input_once(game, pg.K_RETURN) and not game.scene.state:
        if game.scene.name == 'menu':
            if game.player_1:
                game.set_scene('level_select')
                game.sound.play_sfx('ui_select')
                return
            else:
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

    if input_once(game, pg.K_BACKSPACE):
        if game.scene.name == 'menu' and (game.player_1 or game.player_2):
            game.sound.play_sfx('remove')
            game.player_1 = None
            game.player_2 = None

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

    if input_once(game, pg.K_k) and game.scene.name == 'menu':
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

    if input_once(game, pg.K_F7):
        if game.player_1 is not None:
            game.player_1.set_super()
    if input_once(game, pg.K_F8):
        if game.player_2 is not None:
            game.player_2.set_super()


    # Checking for quitting scene or game
    if keys[pg.K_ESCAPE]:
        game.esc_pressed = True

        if game.scene.name == 'menu':
            if game.escape_tick > game.escape_hold_time:
                game.running = False
            else:
                game.escape_tick += 1
                new_color = (255, 255, 255, min(0 + game.escape_tick * 3, 255))
                game.text.quit_text.set_color(new_color)

        if game.scene.name == 'level_select' and not game.scene.state:
            game.sound.play_sfx('ui_select')
            game.set_scene('menu')

        if game.scene.name == 'round':
            if game.escape_tick > game.escape_hold_time:
                game.escape_tick = 0
                game.set_scene('menu')
                game.game_reset()
            else:
                game.escape_tick += 1
                new_color = (255, 255, 255, min(0 + game.escape_tick * 3, 255))
                game.text.escape_text.set_color(new_color)
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