"""
Class that initializes the main logic of the components stores most game values
"""
from random import randint
from random import choice
from utils.particles import ParticleEmitter

from components.objects.bullet import Bullet
from components.objects.bandit_model import BanditModel
from components.objects.player import Player
from components.objects.ufo import Ufo
from components.text_storage import TextStorage
from components.sound import Sound
from components.controls import handle_events
from components.pool import Pool
from components import level
from components import display

from assets import (TITLE_SPRITE, init_loading, BULLET_CONFIG, CARD_CONFIG, BANDITS_CONFIG)
from config import DATA_FORMAT, PLAYER_COLORS

import pygame as pg
import os
import json

class Game:
    def __init__(self):
        self.data = {}
        self.state = 'menu'
        self.clock = pg.time.Clock()
        self.player_1 = None
        self.player_2 = None
        self.level = None
        self.player_count = 0

        # Screen configuration
        self.FPS = 60
        self.screen_width = 960
        self.screen_height = 620
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.tick = 0

        # Key configuration
        self.keys_pressed = []
        self.key_down = False
        self.esc_pressed = None
        self.debug = False

        # Getting initial classes
        init_loading('creating hazzards', 3)
        self.sound = Sound()
        self.text = TextStorage(self)
        self.ufo = Ufo()

        # Getting pool classes for each object/dynamic class
        self.bullet_pool_dict = {
            "bullet": Pool(Bullet, BULLET_CONFIG, 50),
            "card": Pool(Bullet, CARD_CONFIG, 30)
        }

        self.bandit_pool_dict = {
            "basic": Pool(BanditModel, BANDITS_CONFIG["basic"], 15),
            "skilled": Pool(BanditModel, BANDITS_CONFIG["skilled"], 8),
            "hitman": Pool(BanditModel, BANDITS_CONFIG["hitman"], 3),
            "bomber": Pool(BanditModel, BANDITS_CONFIG["bomber"], 5),
            "shielded": Pool(BanditModel, BANDITS_CONFIG["shielded"], 3),
            "dicer": Pool(BanditModel, BANDITS_CONFIG["dicer"], 3),
            "tipsy": Pool(BanditModel, BANDITS_CONFIG["tipsy"], 3)
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
        self.menu_loop = [35, False]
        self.start_animate = True

        self.escape_tick = 0
        self.escape_hold_time = 180

        self.base_ambush_start = [False, 0, 5, 0, 60, False, 0, 300, False]
        self.base_begin_start = [True, 0, 600]
        self.begin_start = self.base_begin_start[:]
        self.ambush_start = self.base_ambush_start[:]
        self.defeat = False
        self.victory = False

        self.base_defeat_values = [
            False,  # Transition enabled
            0, 120,  # UFO blinking animation timer
            0, 60,  # Screen transition timer
            False,  # Screen clearing condition
            False  # Final check for defeat
        ]

        self.base_victory_values = [
            False,  # Transition enabled
            False,  # Condition for getting the players inside
            False,  # Condition for song to play
            0, 400,  # Ufo flying back to space animation timer
            0, 60,  # Screen transition timer
            0, 60, # Black screen timer
            False,  # Screen clearing condition
            False  # Final check for victory
        ]
        self.victory_transition = self.base_victory_values[:]
        self.defeat_transition = self.base_defeat_values[:]

        # Loading starter configurations
        self.base_level = 1
        self.base_config = 1
        self.loading_tick = 0
        self.loading_interval = randint(1, 2)
        self.loading_tips = [
            'Use + or - keys to change music volume!',
            'Use [ or ] keys to change sound effect volume!',
            'Press 0 to mute/unmute music!',
            'Hold ESC in round to return to menu!',
            'Press BACKSPACE on menu to remove players!',
        ]

    def save_data(self):
        file_path = os.path.join('images/other', f'image_config.json')

        if not os.path.exists(file_path):
            self.data = DATA_FORMAT.copy()

        with open(file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"> Data saved.")

    def load_data(self):
        file_path = os.path.join('images/other', f'image_config.json')

        # Check if filepath doesn't exist and create new file
        if not os.path.exists(file_path):
            print(f'> No existing data found, creating new save file.')
            self.save_data()

        # Try to load existing data without errors
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

                # Check and update missing keys
                updated_data = self.sort_data(data, DATA_FORMAT)
                self.data = updated_data
                print(f"> Data loaded.")
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
        pg.display.set_caption('< WESTERN RAID > v0.62')

        self.load_data()
        self.sound.play('menu', -1)

    def run(self):
        self.initialize()

        while True:
            self.update_state()
            handle_events(self)

            self.clock.tick(self.FPS)
            self.tick += 1

    def load_round(self):
        if self.loading_tick == 0:
            self.text.loading_tip.string = choice(self.loading_tips)
        if self.loading_tick == 1:
            self.level = level.Level(self.base_level, self.base_config, self)

        self.loading_tick += 1

        if self.loading_tick > self.loading_interval:
            self.loading_interval = randint(30, 50)
            self.loading_tick = 0

    def game_reset(self):
        self.sound.play('menu', -1)
        self.state = 'menu'

        # self.ambush_fog.enabled = False
        self.victory_transition = self.base_victory_values[:]
        self.defeat_transition = self.base_defeat_values[:]
        self.ambush_start = self.base_ambush_start[:]
        self.begin_start = self.base_begin_start[:]
        self.text.begin_message.set_blink(False)
        self.ufo = Ufo()
        self.player_1 = None
        self.player_2 = None
        self.player_count = 0

        self.save_data()
    
    def add_player(self, controls):
        if not self.player_1:
            color = PLAYER_COLORS[self.player_count]
            self.player_count += 1
            self.player_1 = Player(controls, self.player_count, color)
            self.player_1.rect.center = ((self.screen_width / 2) - 120, self.screen_height / 2)
            self.sound.play_sfx('join')
        elif not self.player_2 and self.player_1.controls != controls:
            color = PLAYER_COLORS[self.player_count]
            self.player_count += 1
            self.player_2 = Player(controls, self.player_count, color)
            self.player_2.rect.center = ((self.screen_width / 2) + 120, self.screen_height / 2)
            self.sound.play_sfx('join')

    def set_final_score(self, score_type='nil'):
        new_best = 0
        if self.player_1:
            new_best += self.player_1.score
            if self.data[f"level{self.level.index}"]["p1_score"] < self.player_1.score:
                self.data[f"level{self.level.index}"]["p1_score"] = self.player_1.score

        if self.player_2:
            new_best += self.player_2.score
            if self.data[f"level{self.level.index}"]["p2_score"] < self.player_2.score:
                self.data[f"level{self.level.index}"]["p2_score"] = self.player_2.score

        self.data["accumulated_score"] += new_best

        if self.data[f"level{self.level.index}"]["best_score"] < new_best:
            self.data[f"level{self.level.index}"]["best_score"] = new_best

        all_levels_score = 0

        for levels in range(1, 3):
            all_levels_score += self.data[f"level{levels}"]["best_score"]

        if self.data[f"total_score"] < all_levels_score:
            self.data[f"total_score"] = all_levels_score
            self.text.new_best_text.enabled = True
        else:
            self.text.new_best_text.enabled = False

        if score_type == 'victory':
            self.data["victories"] += 1
            if self.level.index + 1 <= 3:
                self.data[f"level{self.level.index + 1}"]["unlocked"] = True
        elif score_type == 'defeat':
            self.data["defeats"] += 1

    # Merged "draw" function with components state to make bullet_sprites possible
    def update_state(self):
        if self.state == 'menu':
            if not self.stars.enabled: self.stars.enabled = True
            if self.win_stars.enabled: self.win_stars.enabled = False

            display.render_menu(self)
        elif self.state == 'level_select':
            display.render_level_select(self)
        elif self.state == 'loading_round':
            self.load_round()
            display.render_loading(self)
        elif self.state == 'round':
            if self.stars.enabled: self.stars.enabled = False

            self.level.run(self)
            display.render_round(self)
        elif self.state == 'victory':
            if not self.win_stars.enabled: self.win_stars.enabled = True
            if self.stars.enabled: self.stars.enabled = False

            display.render_victory(self)
        elif self.state == 'defeat':
            display.render_defeat(self)

        display.always_render(self)
        pg.display.flip()
