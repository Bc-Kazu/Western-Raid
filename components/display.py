from assets import TITLE_SPRITE, TITLE_SPRITE_RECT, TITLE_SPRITE_EYES, UFO_SPRITE, \
    TITLE_SPRITE_EYES_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, TITLE_SPRITE_EYES_RECT2, \
    TITLE_SPRITE2, TITLE_SPRITE_EYES2, UFO_SPRITE2, WIN_SPRITE_EYES, WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT, \
    WIN_SPRITE_EYES_RECT2, DEFEAT_CAGE, DEFEAT_CAGE_RECT,  LEVEL_FRAMES, LEVEL_FRAMES_RECT, LEVEL_ICONS, LEVEL_ICONS_RECT, \
    LEVEL_LOCKS, LEVEL_LOCKS_RECT, WASD_CONTROLS_A, WASD_CONTROLS_B, ARROWS_CONTROLS_A, ARROWS_CONTROLS_B, \
    WASD_RECT_A, ARROWS_RECT_A

import pygame as pg
from utils.colors import Colors
colors = Colors()

def hud_message_update(game, new_text):
    game.sound.play_sfx('ui_select2')
    game.text.HUD_text_list[0] = new_text
    game.text.HUD_text_list[1] = 0
    game.text.HUD_text_list[3] = True

def always_render(game):
    if game.text.HUD_text_list[0] and game.text.HUD_text_list[3]:
        game.text.HUD_text_list[1] += 1
        game.text.HUD_text_list[0].draw(game)

        if game.text.HUD_text_list[1] >= game.text.HUD_text_list[2]:
            game.text.HUD_text_list[3] = False
            game.text.HUD_text_list[1] = 0

def cutscene_draw(game, cutscene_type):
    # Drawing temporary screen for special cutscenes
    if cutscene_type == 'time up':
        game.text.timer_text.current_color = (100, 255, 100)
        time_up_tick = 0

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
    elif cutscene_type == 'rebuild ufo':
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

''' ============================================================= '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN MENU  ========== '''
''' ============================================================= '''
def render_menu(game):
    game.screen.fill(colors.space_blue)
    game.stars.update(game)

    # Draw characters on screen depending on players joined
    if game.player_1:
        game.text.start_text.draw(game)
        game.text.choose_text.set_color_blink(False)
        game.text.choose_text.toggle(False)
        offset1 = 100

        game.text.player1_text.set_position(game.screen_width / 2 - offset1, 350)
        game.text.player2_text.draw(game)

        TITLE_SPRITE_RECT.centerx = game.screen_width / 2 - offset1
        UFO_SPRITE_RECT.centerx = TITLE_SPRITE_RECT.centerx
        TITLE_SPRITE_EYES_RECT.centery = TITLE_SPRITE_RECT.centery
        TITLE_SPRITE_EYES_RECT.centerx = TITLE_SPRITE_RECT.centerx - 4

        game.screen.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
        game.screen.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
        game.screen.blit(UFO_SPRITE, UFO_SPRITE_RECT)
    else:
        game.text.player1_text.set_position(game.screen_width / 2, 350)
        game.text.select_text.draw(game)
        WASD_RECT_A.center = (game.screen_width / 2 - 100, 450)
        game.screen.blit(WASD_CONTROLS_A, WASD_RECT_A)

    if game.player_2:
        # Apply position offset
        offset2 = -100

        TITLE_SPRITE_RECT2.centerx = game.screen_width / 2 - offset2
        UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
        TITLE_SPRITE_EYES_RECT2.centery = TITLE_SPRITE_RECT2.centery
        TITLE_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

        game.screen.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
        game.screen.blit(TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2)
        game.screen.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)
    else:
        if game.player_1 and game.player_1.controls != 'WASD':
            WASD_RECT_A.center = (game.screen_width / 2 + 100, 450)
            game.screen.blit(WASD_CONTROLS_A, WASD_RECT_A)
        else:
            ARROWS_RECT_A.center = (game.screen_width / 2 + 100, 450)
            game.screen.blit(ARROWS_CONTROLS_A, ARROWS_RECT_A)


    game.text.title_text.draw(game)
    game.text.volume_text.draw(game)
    game.text.full_score_text.rect = (game.screen_width / 2, 180)
    game.text.full_score_text.string = str("TOTAL SCORE: {:07d}".format(game.data["total_score"]))
    game.text.full_score_text.draw(game)
    game.text.new_best_text.draw(game)
    game.text.player1_text.draw(game)

    if game.tick % game.menu_loop[0] == 0:
        if game.menu_loop[1]:
            TITLE_SPRITE_RECT.y -= 15
            TITLE_SPRITE_EYES_RECT.y -= 15
            UFO_SPRITE_RECT.y -= 15
            TITLE_SPRITE_RECT2.y += 15
            TITLE_SPRITE_EYES_RECT2.y += 15
            UFO_SPRITE_RECT2.y += 15
            game.menu_loop[1] = False
            WASD_CONTROLS_A.set_alpha(150)
            ARROWS_CONTROLS_A.set_alpha(150)
        else:
            TITLE_SPRITE_RECT.y += 15
            TITLE_SPRITE_EYES_RECT.y += 15
            UFO_SPRITE_RECT.y += 15
            TITLE_SPRITE_RECT2.y -= 15
            TITLE_SPRITE_EYES_RECT2.y -= 15
            UFO_SPRITE_RECT2.y -= 15
            game.menu_loop[1] = True
            WASD_CONTROLS_A.set_alpha(255)
            ARROWS_CONTROLS_A.set_alpha(255)


''' ===================================================================== '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN LEVEL SELECT  ========== '''
''' ===================================================================== '''
def render_level_select(game):
    game.screen.fill(colors.space_blue)
    game.stars.update(game)

    game.text.select_tip.draw(game)

    if game.base_level == 1:
        game.text.level1_select.current_color = colors.white
        LEVEL_FRAMES[0].set_alpha(255)
        LEVEL_ICONS[0].set_alpha(255)
    else:
        game.text.level1_select.current_color = (100, 100, 100)
        LEVEL_FRAMES[0].set_alpha(100)
        LEVEL_ICONS[0].set_alpha(150)

    if game.base_level == 2:
        game.text.level2_select.current_color = colors.white
        LEVEL_FRAMES[1].set_alpha(255)
        LEVEL_ICONS[1].set_alpha(255)
    else:
        game.text.level2_select.current_color = (100, 100, 100)
        LEVEL_FRAMES[1].set_alpha(100)
        LEVEL_ICONS[1].set_alpha(100)

    if game.base_level == 3:
        game.text.level3_select.current_color = colors.white
        LEVEL_FRAMES[2].set_alpha(255)
        LEVEL_ICONS[2].set_alpha(255)
    else:
        game.text.level3_select.current_color = (100, 100, 100)
        LEVEL_FRAMES[2].set_alpha(100)
        LEVEL_ICONS[2].set_alpha(100)

    LEVEL_FRAMES[3].set_alpha(100)
    LEVEL_FRAMES[4].set_alpha(100)
    LEVEL_ICONS[3].set_alpha(100)
    LEVEL_ICONS[4].set_alpha(100)

    game.text.level_select.draw(game)
    game.text.level1_select.draw(game)
    game.text.level2_select.draw(game)
    game.text.level3_select.draw(game)
    game.text.level4_select.draw(game)
    game.text.level5_select.draw(game)

    game.screen.blit(LEVEL_FRAMES[0], LEVEL_FRAMES_RECT[0])
    game.screen.blit(LEVEL_FRAMES[1], LEVEL_FRAMES_RECT[1])
    game.screen.blit(LEVEL_FRAMES[2], LEVEL_FRAMES_RECT[2])
    game.screen.blit(LEVEL_FRAMES[3], LEVEL_FRAMES_RECT[3])
    game.screen.blit(LEVEL_FRAMES[4], LEVEL_FRAMES_RECT[4])

    game.screen.blit(LEVEL_ICONS[0], LEVEL_ICONS_RECT[0])
    game.screen.blit(LEVEL_ICONS[1], LEVEL_ICONS_RECT[1])
    game.screen.blit(LEVEL_ICONS[2], LEVEL_ICONS_RECT[2])
    game.screen.blit(LEVEL_ICONS[3], LEVEL_ICONS_RECT[3])
    game.screen.blit(LEVEL_ICONS[4], LEVEL_ICONS_RECT[4])

    for index in range(len(LEVEL_LOCKS)):
        if not game.data[f"level{index + 1}"]["unlocked"]:
            game.screen.blit(LEVEL_LOCKS[index], LEVEL_LOCKS_RECT[index])

    # Draw characters on screen depending on players joined
    if game.player_1:
        game.text.choose_text.set_color_blink(False)
        game.text.choose_text.toggle(False)
        offset1 = 100

        TITLE_SPRITE_RECT.centerx = game.screen_width / 2 - offset1
        UFO_SPRITE_RECT.centerx = TITLE_SPRITE_RECT.centerx
        TITLE_SPRITE_EYES_RECT.centery = TITLE_SPRITE_RECT.centery
        TITLE_SPRITE_EYES_RECT.centerx = TITLE_SPRITE_RECT.centerx - 4

        game.screen.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
        game.screen.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
        game.screen.blit(UFO_SPRITE, UFO_SPRITE_RECT)
    else:
        game.text.select_text.draw(game)
    if game.player_2:
        # Apply position offset
        offset2 = -100

        TITLE_SPRITE_RECT2.centerx = game.screen_width / 2 - offset2
        UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
        TITLE_SPRITE_EYES_RECT2.centery = TITLE_SPRITE_RECT2.centery
        TITLE_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

        game.screen.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
        game.screen.blit(TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2)
        game.screen.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)
    if game.tick % game.menu_loop[0] == 0:
        if game.menu_loop[1]:
            TITLE_SPRITE_RECT.y -= 15
            TITLE_SPRITE_EYES_RECT.y -= 15
            UFO_SPRITE_RECT.y -= 15
            TITLE_SPRITE_RECT2.y += 15
            TITLE_SPRITE_EYES_RECT2.y += 15
            UFO_SPRITE_RECT2.y += 15
            game.menu_loop[1] = False
        else:
            TITLE_SPRITE_RECT.y += 15
            TITLE_SPRITE_EYES_RECT.y += 15
            UFO_SPRITE_RECT.y += 15
            TITLE_SPRITE_RECT2.y -= 15
            TITLE_SPRITE_EYES_RECT2.y -= 15
            UFO_SPRITE_RECT2.y -= 15
            game.menu_loop[1] = True


''' ===================================================================== '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN LEVEL SELECT  ========== '''
''' ===================================================================== '''
loading_dots = '.'
loading_interval = 0

def render_loading(game):
    global loading_dots, loading_interval, loading_tips, tip_interval

    game.screen.fill(colors.space_blue)
    game.stars.update(game)

    loading_interval += 1
    if loading_interval >= 30:
        loading_interval = 0
        loading_dots += '.'

        if len(loading_dots) > 3:
            loading_dots = '.'

        game.text.loading.string = 'Loading' + loading_dots

    game.text.loading.draw(game)
    game.text.loading_tip.draw(game)

''' ============================================================= '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN ROUND ========== '''
''' ============================================================= '''
def render_round(game):
    game.screen.fill(game.level.background_color)
    if game.stars.enabled: game.stars.enabled = False

    # Temporary list for hazzards to be prioritized by their Y position
    draw_queue = []

    for terrain in game.level.map:
        terrain_Zindex = terrain.rect.y + int(terrain.size[1] / 2) if terrain.size[1] < 90 else terrain.rect.y + int(
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
        game.text.p1_points_text.string = str("{:05d}".format(game.player_1.score))
        game.text.p1_points_text.rect = (90, 30)
        game.text.p1_points_text.draw(game)

    if game.player_2:
        game.text.p2_points_text.string = str("{:05d}".format(game.player_2.score))
        game.text.p2_points_text.rect = (game.screen_width - 90, 30)
        game.text.p2_points_text.draw(game)

    if game.ufo.always_on_top:
        game.ufo.draw(game)

    for message in game.level.message_popups:
        message.draw(game)

    time_left = game.level.round_time - game.level.time_elapsed
    seconds = time_left % 60
    minutes = int(time_left / 60) % 60
    game.text.timer_text.string = f'{minutes:02}:{seconds:02}'

    if game.begin_start[0]:
        if game.level.index == 1:
            game.text.begin_message.draw(game)
            game.text.defend_message.draw(game)

        game.begin_start[1] += 1
        p1_control = None
        p2_control = None

        if game.player_1:
            if game.player_1.controls == 'WASD':
                p1_control = WASD_CONTROLS_B
            else:
                p1_control = ARROWS_CONTROLS_B

        if game.player_2:
            if game.player_2.controls == 'WASD':
                p2_control = WASD_CONTROLS_B
            else:
                p2_control = ARROWS_CONTROLS_B

        blink = game.text.begin_message.visible
        if p1_control and game.begin_start[1] < game.begin_start[2] and blink:
            rect = game.player_1.rect
            game.screen.blit(p1_control, (rect.x - 2, rect.y - 50))
        if p2_control and game.begin_start[1] < game.begin_start[2] and blink:
            rect = game.player_2.rect
            game.screen.blit(p2_control, (rect.x - 2, rect.y - 50))

        if game.begin_start[1] >= (game.begin_start[2] / 1.5):
            game.text.begin_message.set_blink(True)
            game.level.can_spawn_early = True
        if game.begin_start[1] >= game.begin_start[2]:
            game.text.begin_message.toggle(False)
        if game.begin_start[1] >= game.begin_start[2] * 1.5:
            game.text.defend_message.set_blink(True)
        if game.begin_start[1] >= game.begin_start[2] * 1.7:
            game.begin_start[0] = False
            game.text.begin_message.toggle(True)
            game.text.begin_message.set_blink(False)
            game.text.defend_message.set_blink(False)


    if not game.victory_transition[0]:
        # Drawing UI
        game.text.timer_text.draw(game)

    ''' AMBUSH MODE PROCESS '''
    if (game.level.time_elapsed > game.level.ambush_time and not game.level.ambush_mode
            and not game.level.victory and not game.level.defeat):
        game.level.ambush_mode = True
        game.ambush_start[5] = True
        game.ambush_start[8] = True
        game.sound.play('BANDIT-RAID', -1)
        game.sound.play_sfx('ambush')

    # game.ambush_fog.update(game)
    if game.level.ambush_mode:
        if not game.ambush_start[0]:
            game.screen.blit(game.ambush_filter, (0, 0))

    # Apply effects on ambush start
    if game.ambush_start[5]:
        game.ambush_start[1] += 1
        game.ambush_start[3] += 1

        if game.ambush_start[1] >= game.ambush_start[2] and game.ambush_start[0]:
            game.ambush_start[1] = 0
            game.ambush_start[0] = False
        elif game.ambush_start[1] >= game.ambush_start[2] and not game.ambush_start[0]:
            game.ambush_start[1] = 0
            game.ambush_start[0] = True
        if game.ambush_start[3] >= game.ambush_start[4]:
            game.ambush_start[5] = False
            game.ambush_start[0] = False
    if game.ambush_start[8] and game.ambush_start[6] <= game.ambush_start[7]:
        game.ambush_start[6] += 1
        game.text.ambush_text.draw(game)

    if game.esc_pressed:
        game.text.escape_text.draw(game)

    # Defeat if ufo is broken, should show a defeat screen with final score
    if not game.ufo.alive and not game.defeat_transition[0]:
        game.defeat_transition[0] = True
        game.sound.play_sfx('ufo_destroy')
        pg.mixer.stop()
    elif time_left < 0 and not game.victory_transition[0]:
        game.victory_transition[0] = True
        game.sound.play('none')
        game.sound.play_sfx('time_up')

        cutscene_draw(game, 'time up')

        # Add points for every block not destroyed at the end
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

                if built: pg.time.delay(int(100 // cooldown_factor))
                cutscene_draw(game, 'rebuild ufo')

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

                cutscene_draw(game, 'rebuild ufo')
            else:
                break

        pg.time.delay(1000)
        game.sound.play('you_should_probably_get_in_the_ufo_now', -1)
        game.sound.play_sfx('ufo_rebuild')


    ''' VICTORY CUTSCENE PROCESS '''
    if game.victory_transition[0]:
        game.level.victory = True
        if game.victory_transition[-1]:
            game.screen.fill((0, 0, 0))
            game.victory_transition[0] = False
            game.sound.play('victory', -1)
            game.state = 'victory'
            game.set_final_score('victory')
        elif not game.victory_transition[1]:
            game.text.get_in.draw(game)
            game.ufo.visible = True
            game.ufo.can_get_in = True
            game.victory_transition[1] = game.ufo.victory_ufo(game.player_1, game.player_2)
        elif game.victory_transition[3] <= game.victory_transition[4]:
            if not game.victory_transition[2]:
                game.sound.play('escape')
                game.victory_transition[2] = True
                game.ufo.can_get_in = False
                game.ufo.always_on_top = True

            game.victory_transition[3] += 1
            game.ufo.victory_ufo(game.player_1, game.player_2)
        elif game.victory_transition[5] <= game.victory_transition[6]:
            game.victory_transition[5] += 1
            game.ufo.visible = False

            if game.victory_transition[5] % 8 == 0 and not game.victory_transition[7]:
                game.screen.fill(colors.space_purple)
                game.victory_transition[7] = True
            elif game.victory_transition[5] % 8 == 0 and game.victory_transition[7]:
                game.screen.fill(game.level.background_color)
                game.victory_transition[7] = False
        elif game.victory_transition[7] <= game.victory_transition[8]:
            game.victory_transition[7] += 1
            game.screen.fill(colors.black)
        else:
            game.ufo.always_on_top = False
            game.screen.fill(colors.black)
            game.victory_transition[9] = False
            game.victory_transition[-1] = True
            UFO_SPRITE_RECT.center = (game.screen_width / 2, 420)
            UFO_SPRITE_RECT2.center = (game.screen_width / 2, 420 + 15)

            TITLE_SPRITE_RECT.center = (game.screen_width / 2, 440)
            WIN_SPRITE_EYES_RECT.center = TITLE_SPRITE_RECT.center
            TITLE_SPRITE_RECT2.center = (game.screen_width / 2, 440 + 15)
            WIN_SPRITE_EYES_RECT2.center = TITLE_SPRITE_RECT2.center


    ''' DEFEAT CUTSCENE PROCESS '''
    if game.defeat_transition[0]:
        if game.defeat_transition[-1]:
            game.defeat_transition[0] = False
            game.sound.play('defeat')
            game.state = 'defeat'
            game.set_final_score('defeat')
        elif game.defeat_transition[1] <= game.defeat_transition[2]:
            game.defeat_transition[1] += 1
            game.ufo.can_blink = True
            if not game.level.defeat:
                game.player_1.set_eyes('shocked_eyes')
                if game.player_2: game.player_2.set_eyes('shocked_eyes')
                game.level.defeat = True
                game.sound.play('none')
                game.sound.play_sfx('ufo_destroy')
        elif game.defeat_transition[3] <= game.defeat_transition[4]:
            game.defeat_transition[3] += 1
            game.ufo.can_blink = False

            if game.defeat_transition[3] % 8 == 0 and not game.defeat_transition[5]:
                game.screen.fill(colors.sad_orange)
                game.defeat_transition[5] = True
            elif game.defeat_transition[3] % 8 == 0 and game.defeat_transition[5]:
                game.screen.fill(game.level.background_color)
                game.defeat_transition[5] = False
        else:
            game.defeat_transition[5] = False
            game.defeat_transition[-1] = True

    if game.debug:
        if game.player_1:
            game.screen.blit(game.player_1.hitbox_area, game.player_1.hitbox)
        if game.player_2:
            game.screen.blit(game.player_2.hitbox_area, game.player_2.hitbox)


''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE VICTORY SCREEN ========= '''
''' ============================================================= '''
def render_victory(game):
    game.screen.fill(colors.space_purple)
    game.win_stars.update(game)

    game.text.survived_text.draw(game)
    game.text.final_message.draw(game)

    final_score = game.player_1.score + (game.player_2.score if game.player_2 else 0)

    game.text.full_score_text.rect = (265, 250)
    game.text.full_score_text.set_text("FINAL SCORE: {:07d}".format(final_score))
    game.text.full_score_text.draw(game)
    game.text.return_text.draw(game)

    # Draw victory stats and players
    if game.player_1:
        game.text.choose_text.set_color_blink(False)
        offset1 = -100
        TITLE_SPRITE_RECT.centerx = game.screen_width / 2 - offset1
        UFO_SPRITE_RECT.centerx = game.screen_width / 2 - offset1
        WIN_SPRITE_EYES_RECT.centerx = (game.screen_width / 2) - 4 - offset1

        game.screen.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
        game.screen.blit(WIN_SPRITE_EYES, WIN_SPRITE_EYES_RECT)
        game.screen.blit(UFO_SPRITE, UFO_SPRITE_RECT)

        game.text.p1_points_text.string = str("PLAYER 1: {:05d}".format(game.player_1.score))
        game.text.p1_points_text.rect = (195, 300)
        game.text.p1_points_text.draw(game)
    if game.player_2:
        # Apply position offset
        offset2 = -300

        TITLE_SPRITE_RECT2.centerx = game.screen_width / 2 - offset2
        UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
        WIN_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

        game.screen.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
        game.screen.blit(WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT2)
        game.screen.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)

        game.text.p2_points_text.string = str("PLAYER 2: {:05d}".format(game.player_2.score))
        game.text.p2_points_text.rect = (200, 350)
        game.text.p2_points_text.draw(game)
    if game.tick % int(game.menu_loop[0] / 1.5) == 0:
        if game.menu_loop[1]:
            TITLE_SPRITE_RECT.y -= 15
            WIN_SPRITE_EYES_RECT.y -= 15
            UFO_SPRITE_RECT.y -= 15
            TITLE_SPRITE_RECT2.y += 15
            WIN_SPRITE_EYES_RECT2.y += 15
            UFO_SPRITE_RECT2.y += 15
            game.menu_loop[1] = False
        else:
            TITLE_SPRITE_RECT.y += 15
            WIN_SPRITE_EYES_RECT.y += 15
            UFO_SPRITE_RECT.y += 15
            TITLE_SPRITE_RECT2.y -= 15
            WIN_SPRITE_EYES_RECT2.y -= 15
            UFO_SPRITE_RECT2.y -= 15
            game.menu_loop[1] = True


''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE DEFEAT SCREEN  ========= '''
''' ============================================================= '''
def render_defeat(game):
    game.screen.fill(colors.sad_orange)
    game.text.lost_text.draw(game)
    game.text.full_score_text.rect = (265, 250)
    game.text.full_score_text.string = str("FINAL SCORE: {:07d}".format(game.data["total_score"]))
    game.text.full_score_text.draw(game)
    game.text.return_text.draw(game)

    # Draw defeat stats and players
    if game.player_2:
        game.player_1.set_offset([-50, 0], [-2, 2])
        game.player_2.set_offset([50, 0], [2, 2])
        game.player_2.draw(game)
        game.player_1.draw(game)
    else:
        game.player_1.set_offset(None, [-2, 2])
        game.player_1.draw(game)

    game.screen.blit(DEFEAT_CAGE, DEFEAT_CAGE_RECT)
