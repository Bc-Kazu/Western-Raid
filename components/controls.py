"""
Module that handles all input interactions with the game
"""
from components.display import hud_message_update
from assets import WASD_RECT_A, ARROWS_RECT_A, LEVEL_FRAMES, LEVEL_FRAMES_RECT

import pygame as pg
import sys

sound_key_table = [pg.K_PLUS, pg.K_EQUALS, pg.K_MINUS, pg.K_LEFTBRACKET, pg.K_RIGHTBRACKET, pg.K_LEFTPAREN, pg.K_RIGHTPAREN]

def handle_events(game):
    keys = pg.key.get_pressed()
    game.keys_pressed = keys
    mouse_down = False

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            game.running = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_down = False

        if event.type == pg.KEYDOWN:
            game.key_down = True
        if event.type == pg.KEYUP:
            game.key_down = False

            if event.key == pg.K_ESCAPE:
                game.escape_tick = 0
                game.text.escape_text.set_color((255, 255, 255))


    # ========== UI Button interactions ========== #
    mouse_pos = pg.mouse.get_pos()

    if mouse_down and game.state == 'menu':
        if WASD_RECT_A.collidepoint(mouse_pos):
            game.add_player('WASD')
        if ARROWS_RECT_A.collidepoint(mouse_pos):
            game.add_player('ARROWS')

    if mouse_down and game.state == 'level_select':
        for level in range(len(LEVEL_FRAMES)):
            rect = LEVEL_FRAMES[level].get_rect()
            rect.topleft = LEVEL_FRAMES_RECT[level]

            if rect.collidepoint(mouse_pos):
                if level + 1 <= 3:
                    if game.base_level != level + 1:
                        game.sound.play_sfx('ui_select')
                        game.base_level = level + 1
                    else:
                        game.sound.play_sfx('start')
                        game.base_config = game.base_level
                        game.state = 'loading_round'
                else:
                    game.sound.play_sfx('push')

    if game.key_down and (game.state == 'menu' or game.state == 'level_select'):
        return

    # Detecting player joining the components
    if game.state == 'menu' or game.state == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            game.add_player('WASD')
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            game.add_player('ARROWS')

    if game.state == 'level_select':
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if game.base_level < 3:
                game.base_level += 1
                game.sound.play_sfx('ui_select')
            else:
                game.base_level = 3
                game.sound.play_sfx('push')
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if game.base_level > 1:
                game.base_level -= 1
                game.sound.play_sfx('ui_select')
            else:
                game.base_level = 1

    if keys[pg.K_RETURN]:
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
        if game.state == 'level_select':
            if game.player_1:
                if not game.data[f"level{game.base_level}"]["unlocked"]:
                    game.sound.play_sfx('push')
                    return

                game.base_config = game.base_level
                game.state = 'loading_round'
                game.sound.play_sfx('start')
            else:
                game.text.choose_text.toggle(True)
                game.text.choose_text.set_color_blink(True)
                hud_message_update(game, game.text.choose_text)
                game.sound.play_sfx('push')
        if game.state == 'victory' or game.state == 'defeat':
            game.sound.play_sfx('ui_select')
            game.game_reset()

    if keys[pg.K_BACKSPACE]:
        if game.state == 'menu' and (game.player_1 or game.player_2):
            game.player_count = 0
            game.sound.play_sfx('remove')
            game.player_1 = None
            game.player_2 = None

    if keys[pg.K_F7] and not game.key_down:
        if game.state == 'round' and game.player_1 is not None:
            game.player_1.set_super()
    if keys[pg.K_F8] and not game.key_down:
        if game.state == 'round' and game.player_2 is not None:
            game.player_2.set_super()

    if keys[pg.K_ESCAPE]:
        game.esc_pressed = True

        if game.state == 'level_select':
            game.sound.play_sfx('ui_select')
            game.state = 'menu'
        elif game.state == 'round':
            if game.escape_tick > game.escape_hold_time:
                game.escape_tick = 0
                game.state = 'menu'
                game.game_reset()
                game.text.escape_text.current_color = (255, 255, 255)
            else:
                game.escape_tick += 1
                game.text.escape_text.current_color = (255 - game.escape_tick, 255, 255 - game.escape_tick)

    else:
        game.esc_pressed = False

    if game.key_down: return

    if keys[pg.K_F3]:
        if game.debug: game.text.debug.set_text(f'DEBUG [ OFF ]')
        else: game.text.debug.set_text(f'DEBUG [ ON ]')
        hud_message_update(game, game.text.debug)
        game.debug = not game.debug

    if keys[pg.K_0]:
        if game.sound.mute: game.text.muted.set_text(f'MUTE [ DISABLED ]')
        else: game.text.muted.set_text(f'MUTE [ ENABLED ]')
        hud_message_update(game, game.text.muted)
        game.sound.mute_music()

    if keys[pg.K_EQUALS] or keys[pg.K_PLUS]:
        game.sound.change_volume('increase')
        game.text.music_change_vol.set_text(f'+ Music: {int(10 * game.sound.volume_offset)}')
        hud_message_update(game, game.text.music_change_vol)
    if keys[pg.K_MINUS]:
        game.sound.change_volume('decrease')
        game.text.music_change_vol.set_text(f'- Music: {int(10 * game.sound.volume_offset)}')
        hud_message_update(game, game.text.music_change_vol)
    if keys[pg.K_RIGHTBRACKET] or keys[pg.K_RIGHTPAREN]:
        game.sound.change_volume_sfx('increase')
        game.text.sfx_change_vol.set_text(f'+ SFX: {int(10 * game.sound.sfx_offset)}')
        hud_message_update(game, game.text.sfx_change_vol)
    if keys[pg.K_LEFTBRACKET] or keys[pg.K_LEFTPAREN]:
        game.sound.change_volume_sfx('decrease')
        game.text.sfx_change_vol.set_text(f'- SFX: {int(10 * game.sound.sfx_offset)}')
        hud_message_update(game, game.text.sfx_change_vol)