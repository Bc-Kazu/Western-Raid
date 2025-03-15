"""
Class that initializes the main logic of the components stores most game values
"""

from components.scenes.defeat import Defeat
from components.scenes.level_select import LevelSelect
from components.scenes.loading import Loading
from components.scenes.menu import Menu
from components.scenes.victory import Victory
from utils.particles import ParticleEmitter

from components.scenes.round import Round

from components.objects.bullet import Bullet
from components.objects.player import Player
from components.objects.ufo import Ufo
from components.text_storage import TextStorage
from components.sound import Sound
from components.controls import handle_events
from components.pool import Pool
from components import level

from components.objects.bandit_types import (
    basic, bomber, dicer, hitman, shielded, skilled, tipsy, boomstick, robber, tangler)

from assets import (TITLE_SPRITE, init_loading, LEVEL_FRAMES, BULLET_CONFIG, CARD_CONFIG, BANDITS_CONFIG,
                    DYNAMITE_CONFIG, BLOCK_CACHE)
from config import DATA_FORMAT, PLAYER_COLORS, ALLOWED_LEVELS

import pygame as pg
import os
import json
import zlib

class Game:
    def __init__(self):
        self.data = {}
        self.scene = None
        self.clock = pg.time.Clock()
        self.player_1 = None
        self.player_2 = None
        self.level = None
        self.player_count = 0

        # Screen and game loop configuration
        self.running = True
        self.FPS = 60
        self.screen_width = 960
        self.screen_height = 620
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.screen_limit = pg.Rect(0, 0, self.screen_width, self.screen_height)
        self.tick = 0

        # Key configuration
        self.keys_pressed = []
        self.debug = False
        self.key_ui_pressed = False

        # Getting initial classes
        init_loading('creating hazzards', 3)
        self.sound = Sound()
        self.text = TextStorage(self)
        self.ufo = Ufo()

        self.scene_dict = {
            'menu': Menu,
            'level_select': LevelSelect,
            'loading': Loading,
            'round': Round,
            'victory': Victory,
            'defeat': Defeat,
        }

        # Getting pool classes for each object/dynamic class
        self.bullet_pool_dict = {
            "bullet": Pool(Bullet, BULLET_CONFIG, 50),
            "card": Pool(Bullet, CARD_CONFIG, 30),
            "dynamite": Pool(Bullet, DYNAMITE_CONFIG, 30),
        }

        self.bandit_pool_dict = {
            "basic": Pool(basic.Bandit, BANDITS_CONFIG["basic"], 15),
            "skilled": Pool(skilled.Bandit, BANDITS_CONFIG["skilled"], 8),
            "tipsy": Pool(tipsy.Bandit, BANDITS_CONFIG["tipsy"], 8),
            "bomber": Pool(bomber.Bandit, BANDITS_CONFIG["bomber"], 5),
            "shielded": Pool(shielded.Bandit, BANDITS_CONFIG["shielded"], 5),
            "dicer": Pool(dicer.Bandit, BANDITS_CONFIG["dicer"], 5),
            "boomstick": Pool(boomstick.Bandit, BANDITS_CONFIG["boomstick"], 5),
            "tangler": Pool(tangler.Bandit, BANDITS_CONFIG["tangler"], 5),
            "hitman": Pool(hitman.Bandit, BANDITS_CONFIG["hitman"], 3),
            "robber": Pool(robber.Bandit, BANDITS_CONFIG["robber"], 3),
        }

        init_loading('creating particles', 1, True)
        # Particle classes
        self.stars = ParticleEmitter(None, (200, 200, 200, 130))
        self.stars.random_alpha = [True, 80]

        self.win_stars = ParticleEmitter(None, (150, 150, 150, 200))
        self.win_stars.random_color = [True, False, 100]
        self.win_stars.random_alpha = [True, 50]
        self.win_stars.fading[1] = 0.5
        self.win_stars.lifetime = [5, 8]
        self.win_stars.size = [5, 15]
        self.win_stars.direction_x = [2, 7]
        self.win_stars.screen_posx = [-500, self.screen_width - 600]
        self.win_stars.rate = 12
        init_loading('finalizing...')

        self.ambush_filter = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        self.ambush_filter.fill((180, 80, 0, 50))

        # These lists are used for "animations" or effects
        self.start_animate = True

        self.esc_pressed = False
        self.escape_tick = 0
        self.escape_hold_time = 90

        self.defeat = False
        self.victory = False
        self.player_bobbing = 10
        self.player_menu_y = 460

        # Loading starter configurations
        self.title_name = '< WESTERN RAID >'
        self.music = 'menu'
        self.base_level = 1
        self.base_config = 1
        self.block_skin = 'block'
        self.broken_skin = 'broken'
        self.ufo_block_config = {}
        self.set_block()

        for i in LEVEL_FRAMES.keys():
            if not i in ALLOWED_LEVELS:
                LEVEL_FRAMES[i].fill((255, 0, 0), special_flags=pg.BLEND_RGBA_MULT)


    def save_data(self):
        file_path = os.path.join('components', 'contentlib.wb')

        if not os.path.exists(file_path):
            self.data = DATA_FORMAT.copy()

        dados_json = json.dumps(self.data)
        dados_comprimidos = zlib.compress(dados_json.encode())

        with open(file_path, "wb") as f:
            print(f'> Saving user data for Western Raid.')
            f.write(dados_comprimidos)

    def load_data(self):
        file_path = os.path.join('components', f'contentlib.wb')
        print(f'> Loading user data for Western Raid.')

        # Check if filepath doesn't exist and create new file
        if not os.path.exists(file_path):
            print(f'> No existing data found, creating new save file.')
            self.save_data()

        # Try to load existing data without errors
        try:
            with open(file_path, "rb") as file:
                data_fetched = file.read()
                decompiled_data = zlib.decompress(data_fetched).decode()
                data = json.loads(decompiled_data)

                # Check and update missing keys
                updated_data = self.sort_data(data, DATA_FORMAT)
                self.data = updated_data
                self.data[f"level1"]["unlocked"] = True
                self.data[f"level2"]["unlocked"] = True
                self.data[f"level3"]["unlocked"] = True
        except json.JSONDecodeError:
            print("Error reading player file, check for any problems in the file"
                  "\nor delete it so a new one can be created.")
            self.data = DATA_FORMAT.copy()

    def sort_data(self, data, template):
        # Recursively update missing keys based on the template
        if not isinstance(data, dict):
            print("> Invalid data format. Resetting to default.")
            return template.copy()

        for key, value in template.items():
            if key not in data:
                print(f"> Adding missing key: {key}")
                data[key] = value
            elif isinstance(value, dict):
                # Recursively check nested dictionaries
                data[key] = self.sort_data(data.get(key, {}), value)

        return data

    def initialize(self):
        # Setting up the display window customization
        pg.display.set_icon(TITLE_SPRITE)
        pg.display.set_caption('< WESTERN RAID > v0.7.2')

        self.load_data()
        self.set_scene('menu')
        self.sound.play(self.music, -1)

    def set_scene(self, name):
        self.scene = self.scene_dict[name](name, self.screen)

        if self.scene.name == 'menu':
            self.scene.set_title(self)

    def set_music(self, name):
        self.music = name
        self.sound.play(name, -1)

    def set_block(self, block='block', broken='broken'):
        self.block_skin = block
        self.broken_skin = broken
        self.ufo_block_config = {
            'name': 'ufo_block',
            'type': 'block',
            'size': (25, 25),
            'image': BLOCK_CACHE[block].copy(),
            'broken_image': BLOCK_CACHE[broken].copy()
        }

    def run(self):
        while self.tick < 200:
            self.stars.update(self)
            self.win_stars.update(self)
            self.tick += 1

        self.initialize()

        while self.running:
            self.update_state()
            handle_events(self)

            self.tick += 1
            self.clock.tick(self.FPS)

    def game_reset(self):
        self.sound.play(self.music, -1)
        self.set_scene('menu')

        self.text.begin_message.set_blink(False)
        self.ufo = Ufo()
        self.player_1 = None
        self.player_2 = None
        self.player_count = 0

        self.save_data()
    
    def add_player(self, controls):
        if not self.player_1:
            self.player_count = 1
            color = PLAYER_COLORS[0]
            self.player_1 = Player(controls, self.player_count, color)
            self.sound.play_sfx('join')
        elif not self.player_2 and self.player_1.controls != controls:
            self.player_count = 2
            color = PLAYER_COLORS[1]
            self.player_2 = Player(controls, self.player_count, color)
            self.sound.play_sfx('join')

    def start_round(self):
        if self.level:
            self.set_scene('round')
            self.scene.reset()
            self.scene.set_state('init_cutscene')

    def enter_level(self):
        if self.data[f'level{self.base_level}']['unlocked']:
            self.scene.set_state('start')
        else:
            self.sound.play_sfx('push')

    def start_loading(self):
        self.base_config = self.base_level
        self.set_scene('loading')

    def load_level(self):
        self.level = level.Level(self.base_level, self.base_config, self)

    def set_level(self, level_index, is_mouse=False):
        # Only allow levels avaliable in list
        if level_index in ALLOWED_LEVELS:
            if self.base_level != level_index:
                self.sound.play_sfx('ui_select')
                self.base_level = level_index
            elif is_mouse:
                self.enter_level()
        else:
            self.sound.play_sfx('push')

    def set_final_score(self, score_type='nil'):
        level_score = 0
        lv = self.level.index

        for plr in [self.player_1, self.player_2]:
            if not plr:
                continue

            level_score += plr.score
            if self.data[f"level{lv}"][f"p{plr.id}_score"] < plr.score:
                self.data[f"level{lv}"][f"p{plr.id}_score"] = plr.score

        self.data["accumulated_score"] += level_score

        if self.data[f"level{lv}"]["best_score"] < level_score:
            self.data[f"level{lv}"]["best_score"] = level_score

        full_score = 0

        for levels in ALLOWED_LEVELS:
            full_score += self.data[f"level{levels}"]["best_score"]

        new_best = self.data[f"total_score"] < full_score
        self.text.new_best_text.enabled = new_best
        self.data[f"total_score"] = full_score if new_best else self.data[f"total_score"]

        if score_type == 'victory':
            self.data[f"level{lv}"]["wins"] += 1
            if lv + 1 in ALLOWED_LEVELS:
                self.data[f"level{lv + 1}"]["unlocked"] = True
        elif score_type == 'defeat':
            self.data[f"level{lv}"]["defeats"] += 1

    def set_hud(self, new_text):
        self.sound.play_sfx('ui_select2')
        self.text.HUD_text_list[0] = new_text
        self.text.HUD_text_list[1] = 0
        self.text.HUD_text_list[3] = True

    def always_render(self):
        if self.text.HUD_text_list[0] and self.text.HUD_text_list[3]:
            self.text.HUD_text_list[1] += 1
            self.text.HUD_text_list[0].draw(self)

            if self.text.HUD_text_list[1] >= self.text.HUD_text_list[2]:
                self.text.HUD_text_list[3] = False
                self.text.HUD_text_list[1] = 0

    def players_animate(self, ufo_dict, player_offset):
        for player in [self.player_1, self.player_2]:
            if not player:
                continue

            new_x = self.screen_width // 2 + player_offset[player.id]
            new_y = self.player_menu_y
            new_y -= self.player_bobbing if player.id % 2 == 0 else -self.player_bobbing

            player.set_offset(None, [-4, 0])
            player.set_position(new_x, new_y, True)
            player.draw(self)

            ufo = ufo_dict[player.id]
            ufo[1].center = (new_x, new_y - 20)
            self.screen.blit(ufo[0], ufo[1])


    # Merged "draw" function with components state to make bullet_sprites possible
    def update_state(self):
        if self.scene.name == 'round':
            self.level.run(self)

        self.scene.draw(self)
        self.always_render()
        pg.display.flip()
