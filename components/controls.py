"""
Module that handles all input interactions with the game
"""
from components.display import hud_message_update
from assets import WASD_RECT_A, ARROWS_RECT_A, LEVEL_FRAMES, LEVEL_FRAMES_RECT, UFO_SPRITE_RECT, UFO_SPRITE_RECT2

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
                game.text.escape_text.set_color((255, 255, 255))


    # ========== UI Button interactions ========== #
    mouse_pos = pg.mouse.get_pos()

    if game.state == 'menu':
        if mouse_input == mouse_states['left']:
            if UFO_SPRITE_RECT.collidepoint(mouse_pos) and game.player_1:
                game.state = 'level_select'
                game.sound.play_sfx('ui_select')
            if UFO_SPRITE_RECT2.collidepoint(mouse_pos) and game.player_2:
                game.state = 'level_select'
                game.sound.play_sfx('ui_select')

            if WASD_RECT_A.collidepoint(mouse_pos):
                game.add_player('WASD')
            if ARROWS_RECT_A.collidepoint(mouse_pos):
                game.add_player('ARROWS')
        elif mouse_input == mouse_states['right']:
            if UFO_SPRITE_RECT.collidepoint(mouse_pos) and game.player_1:
                game.player_1 = None
                game.player_2 = None
                game.player_count = 0
                game.sound.play_sfx('remove')
            if UFO_SPRITE_RECT2.collidepoint(mouse_pos) and game.player_2:
                game.player_2 = None
                game.player_count = 1
                game.sound.play_sfx('remove')

    if mouse_input == 1 and game.state == 'level_select':
        for level in range(len(LEVEL_FRAMES)):
            rect = LEVEL_FRAMES[level].get_rect()
            rect.topleft = LEVEL_FRAMES_RECT[level]

            if rect.collidepoint(mouse_pos):
                game.set_level(level + 1, True)

    # Detecting player joining the components
    if game.state == 'menu' or game.state == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            game.add_player('WASD')
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            game.add_player('ARROWS')

    if game.state == 'level_select':
        if input_once(game, pg.K_RIGHT) or input_once(game, pg.K_d):
            game.set_level(game.base_level + 1)
        if input_once(game, pg.K_LEFT) or input_once(game, pg.K_a):
            game.set_level(game.base_level - 1)

    if input_once(game, pg.K_RETURN):
        if game.state == 'menu':
            if game.player_1:
                game.state = 'level_select'
                game.sound.play_sfx('ui_select')
                return
            else:
                game.text.choose_text.toggle(True)
                game.text.choose_text.set_color_blink(True)
                hud_message_update(game, game.text.choose_text)
                game.sound.play_sfx('push')

        # Starting level if possible
        if game.state == 'level_select' and game.player_1:
            game.start_round()
        if game.state == 'victory' or game.state == 'defeat':
            game.sound.play_sfx('ui_select')
            game.game_reset()

    if input_once(game, pg.K_BACKSPACE):
        if game.state == 'menu' and (game.player_1 or game.player_2):
            game.sound.play_sfx('remove')
            game.player_1 = None
            game.player_2 = None

    if input_once(game, pg.K_F7):
        if game.state == 'round' and game.player_1 is not None:
            game.player_1.set_super()
    if input_once(game, pg.K_F8):
        if game.state == 'round' and game.player_2 is not None:
            game.player_2.set_super()

    if input_once(game, pg.K_ESCAPE):
        game.esc_pressed = True

        if game.state == 'level_select':
            game.sound.play_sfx('ui_select')
            game.state = 'menu'

    # Checking for quitting round
    if keys[pg.K_ESCAPE]:
        if game.state == 'round':
            if game.escape_tick > game.escape_hold_time:
                game.escape_tick = 0
                game.state = 'menu'
                game.game_reset()
                game.text.escape_text.current_color = (255, 255, 255)
            else:
                game.escape_tick += 1
                game.text.escape_text.current_color = (
                    255,
                    255 - game.escape_tick,
                    255 - game.escape_tick * 3
                )
    else:
        game.esc_pressed = False

    if input_once(game, pg.K_F3):
        if game.debug: game.text.debug.set_text(f'DEBUG [ OFF ]')
        else: game.text.debug.set_text(f'DEBUG [ ON ]')
        hud_message_update(game, game.text.debug)
        game.debug = not game.debug
    elif input_once(game, pg.K_0):
        if game.sound.mute: game.text.muted.set_text(f'MUTE [ DISABLED ]')
        else: game.text.muted.set_text(f'MUTE [ ENABLED ]')
        hud_message_update(game, game.text.muted)
        game.sound.mute_music()
    elif input_once(game, pg.K_EQUALS) or input_once(game, pg.K_PLUS):
        game.sound.change_volume('increase')
        game.text.music_change_vol.set_text(f'+ Music: {int(10 * game.sound.volume_offset)}')
        hud_message_update(game, game.text.music_change_vol)
    elif input_once(game, pg.K_MINUS):
        game.sound.change_volume('decrease')
        game.text.music_change_vol.set_text(f'- Music: {int(10 * game.sound.volume_offset)}')
        hud_message_update(game, game.text.music_change_vol)
    elif input_once(game, pg.K_RIGHTBRACKET) or input_once(game, pg.K_RIGHTPAREN):
        game.sound.change_volume_sfx('increase')
        game.text.sfx_change_vol.set_text(f'+ SFX: {int(10 * game.sound.sfx_offset)}')
        hud_message_update(game, game.text.sfx_change_vol)
    elif input_once(game, pg.K_LEFTBRACKET) or input_once(game, pg.K_LEFTPAREN):
        game.sound.change_volume_sfx('decrease')
        game.text.sfx_change_vol.set_text(f'- SFX: {int(10 * game.sound.sfx_offset)}')
        hud_message_update(game, game.text.sfx_change_vol)