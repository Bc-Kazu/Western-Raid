"""
Module for loading and configuring components assets.

This module handles the initialization of fonts and the loading and transformation
of image resources. It centralizes asset management to keep the main code clean.
"""
import sys

import pygame as pg
import os
import inspect
from utils.text import Text
from utils.colors import Colors
from config import POWER_UPS, ITEMS, BRICKS
colors = Colors()
pg.init()

# Temporary scren values, do not use these in other files
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def get_line_number():
    """Returns the current line number in the script."""
    return inspect.currentframe().f_back.f_lineno

# Font configuration
SMALL_FONT = pg.font.Font("assets/retro_font.ttf", 16)
TEXT_FONT = pg.font.Font("assets/retro_font.ttf", 24)
NORMAL_FONT = pg.font.Font("assets/retro_font.ttf", 40)
TITLE_FONT = pg.font.Font("assets/retro_font.ttf", 72)

INIT_LOADING_TEXT = Text('LOADING GAME...', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), NORMAL_FONT, (150, 158, 170))
INIT_LOADING_DESC = Text('', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.75), TEXT_FONT, colors.dark_grey)

loading_progress = 0
def init_loading(string, progress=None, reset_progress=False):
    global INIT_LOADING_TEXT, INIT_LOADING_DESC, loading_progress
    pg.event.pump()
    loading_progress += progress if progress else 0
    string = f'{string} ({loading_progress})' if progress else f'{string}'

    SCREEN.fill((0, 0, 0))
    INIT_LOADING_DESC.set_text(string)
    INIT_LOADING_DESC.draw(None, SCREEN)
    INIT_LOADING_TEXT.draw(None, SCREEN)
    pg.display.flip()

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if reset_progress:
        loading_progress = 0

supported_formats = ["bmp", "png", "jpg", "jpeg", "gif", "tga", "webp"]
def load_images_from_folder(folder_path, image_cache):
    """Loads all images from a folder into the image cache dictionary."""
    for filename in os.listdir(folder_path):
        if "." in filename and filename.rsplit(".", 1)[1] in supported_formats:
            image_name = filename.rsplit(".", 1)[0]
            image_cache[image_name] = pg.image.load(os.path.join(folder_path, filename)).convert_alpha()
            init_loading('loading assets', 1)

# Preloading all images that are added/removed through the game
BANDIT_CACHE = {}
BULLET_CACHE = {}
DECORATION_CACHE = {}
ITEM_CACHE = {}
TERRAIN_CACHE = {}
UI_CACHE = {}
BLOCK_CACHE = {}
GADGET_CACHE = {}

load_images_from_folder("assets/bandit_sprites", BANDIT_CACHE)
load_images_from_folder("assets/bullet_sprites", BULLET_CACHE)
load_images_from_folder("assets/decoration_sprites", DECORATION_CACHE)
load_images_from_folder("assets/item_sprites", ITEM_CACHE)
load_images_from_folder("assets/terrain_sprites", TERRAIN_CACHE)
load_images_from_folder("assets/ui_sprites", UI_CACHE)
load_images_from_folder("assets/block_sprites", BLOCK_CACHE)
load_images_from_folder("assets/gadget_sprites", GADGET_CACHE)
EMPTY_IMAGE = pg.image.load('assets/nil.png')

BASE_PLAYER_SIZE = (50, 50)
P2_TITLE_OFFSET = 15

PLAYER1_IMAGE = pg.image.load(f'assets/player_sprites/1/body.png').convert_alpha()
init_loading('loading assets', 3)

PLAYER_CONFIG = {
    'name': 'player',
    'type': 'player',
    'size': BASE_PLAYER_SIZE,
}

BULLET_CONFIG = {
    'name': 'bullet',
    'type': 'bullet',
    'size': (8, 8),
    'color': colors.white,
    'image': BULLET_CACHE['bullet']
}

CARD_CONFIG = {
    'name': 'card',
    'type': 'bullet',
    'size': (14, 14),
    'color': colors.white,
    'image': BULLET_CACHE['card']
}

DYNAMITE_CONFIG = {
    'name': 'dynamite',
    'type': 'bullet',
    'size': (26, 26),
    'color': colors.coral,
    'image': BULLET_CACHE['dynamite']
}

TERRAIN_CONFIG = {'name': 'any', 'type': 'terrain','size': (180, 180)}

EXPLOSION_CONFIG = {
    'name': 'explosion',
    'type': 'threat',
    'size': (50, 50),
    'color': colors.white,
    'image': BULLET_CACHE['bullet']
}

POISON_CONFIG = {
    'name': 'poison',
    'type': 'threat',
    'size': (50, 50),
    'color': colors.white,
    'image': BULLET_CACHE['poison']
}

UFO_SPRITE = pg.image.load('assets/ui_sprites/UFO.png').convert_alpha()
UFO_SPRITE = pg.transform.scale(UFO_SPRITE, (150, 150))
UFO_SPRITE_RECT = UFO_SPRITE.get_rect()
UFO_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 420)
init_loading('loading assets', 5)

UFO_CONFIG = {
    'name': 'spaceship',
    'type': 'ufo',
    'size': (180, 180),
    'color': colors.light_blue,
    'image': UFO_SPRITE.copy()
}

UFO_BLOCK_CONFIG = {
    'name': 'ufo_block',
    'type': 'block',
    'size': (25, 25),
    'image': BLOCK_CACHE['block'].copy(),
    'image_2': BLOCK_CACHE['broken'].copy()
}

TURRET_SHOOTER_CONFIG = {
    'name': 'turret_shooter',
    'type': 'gadget',
    'size': (60, 60),
    'image': GADGET_CACHE['turret_shooter'].copy(),
}

TURRET_SHIELD_CONFIG = {
    'name': 'turret_shield',
    'type': 'gadget',
    'size': (60, 60),
    'image': GADGET_CACHE['turret_shield'].copy(),
}

BOT_SHOOTER_CONFIG = {
    'name': 'bot_shooter',
    'type': 'gadget',
    'size': (40, 40),
    'image': GADGET_CACHE['bot_shooter'].copy(),
}

LUCK_STATUE = {'name': 'luck_statue', 'type': 'terrain', 'size': (75, 75),
              'color': colors.burnt_amber, 'image': TERRAIN_CACHE['luck_statue'].copy()}

BANDITS_CONFIG = {
    "basic": {'name': 'basic', 'type': 'enemy', 'size': (60, 60),
              'color': colors.white, 'image': BANDIT_CACHE['basic'].copy()},
    "skilled": {'name': 'skilled', 'type': 'enemy', 'size': (60, 60),
                     'color': colors.white, 'image': BANDIT_CACHE['skilled'].copy()},
    "hitman": {'name': 'hitman', 'type': 'enemy', 'size': (60, 60),
                     'color': colors.white, 'image': BANDIT_CACHE['hitman'].copy()},
    "bomber": {'name': 'bomber', 'type': 'enemy', 'size': (70, 70),
                     'color': colors.white, 'image': BANDIT_CACHE['bomber'].copy()},
    "shielded": {'name': 'shielded', 'type': 'enemy', 'size': (60, 60),
                     'color': colors.white, 'image': BANDIT_CACHE['basic'].copy()},
    "dicer": {'name': 'dicer', 'type': 'enemy', 'size': (50, 50),
                     'color': colors.white, 'image': BANDIT_CACHE['dicer'].copy()},
    "tipsy": {'name': 'tipsy', 'type': 'enemy', 'size': (60, 60),
                     'color': colors.white, 'image': BANDIT_CACHE['basic'].copy()},
    "boomstick": {'name': 'boomstick', 'type': 'enemy', 'size': (60, 60),
              'color': colors.white, 'image': BANDIT_CACHE['boomstick'].copy()},
    "bullseye": {'name': 'bullseye', 'type': 'enemy', 'size': (60, 60),
              'color': colors.white, 'image': BANDIT_CACHE['bullseye'].copy()},
    "tangler": {'name': 'tangler', 'type': 'enemy', 'size': (60, 60),
              'color': colors.white, 'image': BANDIT_CACHE['tangler'].copy()},
}
init_loading('loading assets', len(BANDITS_CONFIG))

PICKUPS_CONFIG = {}

for key, file in ITEM_CACHE.items():
    pickup_type = None
    frame_color = colors.white
    despawn_time = 10

    if key in POWER_UPS:
        pickup_type = 'power_up'
        frame_color = colors.hot_pink
        despawn_time = 15
    elif key in ITEMS:
        pickup_type = 'item'
        frame_color = colors.light_yellow
        despawn_time = 12
    elif key in BRICKS:
        pickup_type = 'brick'
    else:
        print(f'Could not find {key} in any pickup list from CONFIG.')
        continue

    PICKUPS_CONFIG[key] = {
        'name': key,
        'type': pickup_type,
        'size': (40, 40),
        'image': file.copy(),
        'frame_color': frame_color,
        'despawn_time': despawn_time
    }

LEVELS_ENVIROMENT = {
    "level1": [
        [10, {'name': 'cactus1', 'type': 'terrain', 'size': (70, 70),
              'color': colors.bush_green, 'image': TERRAIN_CACHE['cactus1'].copy()}],
        [10, {'name': 'cactus2', 'type': 'terrain', 'size': (70, 70),
              'color': colors.bush_green, 'image': TERRAIN_CACHE['cactus2'].copy()}],
        [5, {'name': 'rock', 'type': 'terrain', 'size': (70, 70),
              'color': colors.rock_brown, 'image': TERRAIN_CACHE['rock'].copy()}],
        [3, {'name': 'large_rock', 'type': 'terrain', 'size': (140, 140),
                  'color': colors.rock_brown, 'image': TERRAIN_CACHE['large_rock'].copy()}],
        [7, {'name': 'tumbleweed', 'type': 'terrain', 'size': (70, 70),
                  'color': colors.dead_brown, 'image': TERRAIN_CACHE['tumbleweed'].copy()}],
    ],
    "level2": [
        [50, {'name': 'table', 'type': 'terrain', 'size': (100, 100),
              'color': colors.mundane_orange, 'image': TERRAIN_CACHE['table'].copy()}],
        [20, {'name': 'large_table', 'type': 'terrain', 'size': (200, 200),
              'color': colors.mundane_orange, 'image': TERRAIN_CACHE['large_table'].copy()}],
        [10, {'name': 'broken_table', 'type': 'terrain', 'size': (100, 100),
              'color': colors.mundane_orange, 'image': TERRAIN_CACHE['broken_table'].copy()}],
        [4, {'name': 'jukebox', 'type': 'terrain', 'size': (140, 140),
             'color': colors.saddle_brown, 'image': TERRAIN_CACHE['jukebox'].copy()}],
        [2, {'name': 'arcade_machine', 'type': 'terrain', 'size': (140, 140),
             'color': colors.pale_yellow, 'image': TERRAIN_CACHE['arcade_machine'].copy()}],
    ],
    "level3": [
        [10, {'name': 'rock', 'type': 'terrain', 'size': (70, 70),
              'color': colors.rock_blue, 'image': TERRAIN_CACHE['rock'].copy()}],
        [10, {'name': 'dead_bush', 'type': 'terrain', 'size': (70, 70),
              'color': colors.dead_brown, 'image': TERRAIN_CACHE['dead_bush'].copy()}],
        [8, {'name': 'dead_tree', 'type': 'terrain', 'size': (140, 140),
             'color': colors.plant_brown, 'image': TERRAIN_CACHE['dead_tree'].copy()}],
        [15, {'name': 'fossil1', 'type': 'terrain', 'size': (70, 70),
              'color': colors.grey, 'image': TERRAIN_CACHE['fossil1'].copy()}],
        [15, {'name': 'fossil2', 'type': 'terrain', 'size': (50, 50),
              'color': colors.grey, 'image': TERRAIN_CACHE['fossil2'].copy()}],
        [5, {'name': 'large_fossil', 'type': 'terrain', 'size': (140, 140),
             'color': colors.grey, 'image': TERRAIN_CACHE['large_fossil'].copy()}],
    ]
}
init_loading('loading assets', 30)

# Image configuration
TITLE_SPRITE = pg.image.load('assets/player_sprites/1/body.png').convert_alpha()
TITLE_SPRITE = pg.transform.scale(TITLE_SPRITE, BASE_PLAYER_SIZE)
TITLE_SPRITE_RECT = TITLE_SPRITE.get_rect()
TITLE_SPRITE_RECT.center = (SCREEN_WIDTH // 2, 440)
init_loading('loading assets', 1)

TITLE_SPRITE2 = pg.image.load('assets/player_sprites/2/body.png').convert_alpha()
TITLE_SPRITE2 = pg.transform.scale(TITLE_SPRITE2, BASE_PLAYER_SIZE)
TITLE_SPRITE_RECT2 = TITLE_SPRITE2.get_rect()
TITLE_SPRITE_RECT2.center = (SCREEN_WIDTH // 2, 440 + P2_TITLE_OFFSET)
init_loading('loading assets', 1)

TITLE_SPRITE_EYES = pg.image.load('assets/player_sprites/1/base_eyes.png').convert_alpha()
TITLE_SPRITE_EYES = pg.transform.scale(TITLE_SPRITE_EYES, BASE_PLAYER_SIZE)
TITLE_SPRITE_EYES_RECT = TITLE_SPRITE_EYES.get_rect()
TITLE_SPRITE_EYES_RECT.center = ((SCREEN_WIDTH // 2) - 4, 440)
init_loading('loading assets', 1)

TITLE_SPRITE_EYES2 = pg.image.load('assets/player_sprites/1/base_eyes.png').convert_alpha()
TITLE_SPRITE_EYES2 = pg.transform.scale(TITLE_SPRITE_EYES2, BASE_PLAYER_SIZE)
TITLE_SPRITE_EYES_RECT2 = TITLE_SPRITE_EYES2.get_rect()
TITLE_SPRITE_EYES_RECT2.center = ((SCREEN_WIDTH // 2) - 4, 440 + P2_TITLE_OFFSET)
init_loading('loading assets', 1)

WIN_SPRITE_EYES = pg.image.load('assets/player_sprites/1/happy_eyes.png').convert_alpha()
WIN_SPRITE_EYES = pg.transform.scale(WIN_SPRITE_EYES, BASE_PLAYER_SIZE)
WIN_SPRITE_EYES_RECT = WIN_SPRITE_EYES.get_rect()
WIN_SPRITE_EYES_RECT.center = ((SCREEN_WIDTH // 2) - 4, 440)
init_loading('loading assets', 1)

WIN_SPRITE_EYES2 = pg.image.load('assets/player_sprites/1/happy_eyes.png').convert_alpha()
WIN_SPRITE_EYES2 = pg.transform.scale(WIN_SPRITE_EYES2, BASE_PLAYER_SIZE)
WIN_SPRITE_EYES_RECT2 = WIN_SPRITE_EYES2.get_rect()
WIN_SPRITE_EYES_RECT2.center = ((SCREEN_WIDTH // 2) - 4, 440 + P2_TITLE_OFFSET)
init_loading('loading assets', 1)

UFO_SPRITE2 = pg.image.load('assets/ui_sprites/UFO2.png').convert_alpha()
UFO_SPRITE2 = pg.transform.scale(UFO_SPRITE2, (150, 150))
UFO_SPRITE_RECT2 = UFO_SPRITE2.get_rect()
UFO_SPRITE_RECT2.center = (SCREEN_WIDTH / 2, 420 + P2_TITLE_OFFSET)
init_loading('loading assets', 1)

DEFEAT_CAGE = pg.image.load('assets/ui_sprites/defeat_cage.png').convert_alpha()
DEFEAT_CAGE = pg.transform.scale(DEFEAT_CAGE, (int(110 * 5), int(30 * 5)))
DEFEAT_CAGE_RECT = DEFEAT_CAGE.get_rect()
DEFEAT_CAGE_RECT.center = ((SCREEN_WIDTH // 2), SCREEN_HEIGHT - 200)
init_loading('loading assets', 1)

UI_FRAME = pg.image.load('assets/ui_sprites/ui_frame.png').convert_alpha()
UI_FRAME = pg.transform.scale(UI_FRAME, (100, 100))
init_loading('loading assets', 1)

WASD_CONTROLS_A = pg.image.load('assets/ui_sprites/WASD.png').convert_alpha()
ARROWS_CONTROLS_A = pg.image.load('assets/ui_sprites/ARROWS.png').convert_alpha()
WASD_RECT_A = WASD_CONTROLS_A.get_rect()
ARROWS_RECT_A = WASD_CONTROLS_A.get_rect()
init_loading('loading assets', 1)

WASD_CONTROLS_B = pg.image.load('assets/ui_sprites/WASD.png').convert_alpha()
ARROWS_CONTROLS_B = pg.image.load('assets/ui_sprites/ARROWS.png').convert_alpha()
WASD_CONTROLS_B = pg.transform.scale(WASD_CONTROLS_B, (55, 36))
ARROWS_CONTROLS_B = pg.transform.scale(ARROWS_CONTROLS_B, (55, 36))
WASD_RECT_B = WASD_CONTROLS_B.get_rect()
ARROWS_RECT_B = ARROWS_CONTROLS_B.get_rect()
init_loading('loading assets', 2)

LEVEL_FRAMES = [
    UI_FRAME.copy(),
    UI_FRAME.copy(),
    UI_FRAME.copy(),
    UI_FRAME.copy(),
    UI_FRAME.copy()
]

LEVEL_FRAMES[3].fill((255, 0, 0), special_flags=pg.BLEND_RGBA_MULT)
LEVEL_FRAMES[4].fill((255, 0, 0), special_flags=pg.BLEND_RGBA_MULT)
init_loading('loading assets', 5)

LEVEL_FRAMES_RECT = [
    UI_FRAME.get_rect(),
    UI_FRAME.get_rect(),
    UI_FRAME.get_rect(),
    UI_FRAME.get_rect(),
    UI_FRAME.get_rect()
]

LEVEL_FRAMES_RECT[0] = (100, 170)
LEVEL_FRAMES_RECT[1] = (260, 170)
LEVEL_FRAMES_RECT[2] = (430, 170)
LEVEL_FRAMES_RECT[3] = (590, 170)
LEVEL_FRAMES_RECT[4] = (750, 170)
init_loading('loading assets', 5)

LEVEL_ICONS = [
    TERRAIN_CACHE['cactus1'].copy(),
    TERRAIN_CACHE['arcade_machine'].copy(),
    TERRAIN_CACHE['fossil2'].copy(),
    UI_CACHE['question'].copy(),
    UI_CACHE['question'].copy()
]

LEVEL_ICONS[0] = pg.transform.scale(LEVEL_ICONS[0], (80, 80))
LEVEL_ICONS[1] = pg.transform.scale(LEVEL_ICONS[1], (80, 80))
LEVEL_ICONS[2] = pg.transform.scale(LEVEL_ICONS[2], (80, 80))
LEVEL_ICONS[3] = pg.transform.scale(LEVEL_ICONS[3], (80, 80))
LEVEL_ICONS[4] = pg.transform.scale(LEVEL_ICONS[4], (80, 80))

LEVEL_ICONS[0].fill((60, 160, 90), special_flags=pg.BLEND_RGBA_MULT)
LEVEL_ICONS[1].fill((155, 130, 80), special_flags=pg.BLEND_RGBA_MULT)
LEVEL_ICONS[2].fill((150, 150, 150), special_flags=pg.BLEND_RGBA_MULT)
LEVEL_ICONS[3].fill((100, 0, 0), special_flags=pg.BLEND_RGBA_MULT)
LEVEL_ICONS[4].fill((100, 0, 0), special_flags=pg.BLEND_RGBA_MULT)
init_loading('loading assets', 5)

LEVEL_ICONS_RECT = [
    LEVEL_ICONS[0].get_rect(),
    LEVEL_ICONS[1].get_rect(),
    LEVEL_ICONS[2].get_rect(),
    LEVEL_ICONS[3].get_rect(),
    LEVEL_ICONS[4].get_rect()
]

LEVEL_ICONS_RECT[0] = (110, 180)
LEVEL_ICONS_RECT[1] = (270, 175)
LEVEL_ICONS_RECT[2] = (440, 180)
LEVEL_ICONS_RECT[3] = (600, 180)
LEVEL_ICONS_RECT[4] = (760, 180)
init_loading('loading assets', 5)

LOCKED_IMAGE = pg.image.load('assets/ui_sprites/locked.png').convert_alpha()

LEVEL_LOCKS = [
    LOCKED_IMAGE.copy(),
    LOCKED_IMAGE.copy(),
    LOCKED_IMAGE.copy(),
    LOCKED_IMAGE.copy(),
    LOCKED_IMAGE.copy()
]

LEVEL_LOCKS[0] = pg.transform.scale(LEVEL_LOCKS[0], (80, 80))
LEVEL_LOCKS[1] = pg.transform.scale(LEVEL_LOCKS[1], (80, 80))
LEVEL_LOCKS[2] = pg.transform.scale(LEVEL_LOCKS[2], (80, 80))
LEVEL_LOCKS[3] = pg.transform.scale(LEVEL_LOCKS[3], (80, 80))
LEVEL_LOCKS[4] = pg.transform.scale(LEVEL_LOCKS[4], (80, 80))
init_loading('loading assets', 5)

LEVEL_LOCKS_RECT = [
    LEVEL_LOCKS[0].get_rect(),
    LEVEL_LOCKS[1].get_rect(),
    LEVEL_LOCKS[2].get_rect(),
    LEVEL_LOCKS[3].get_rect(),
    LEVEL_LOCKS[4].get_rect()
]

LEVEL_LOCKS_RECT[0] = (110, 180)
LEVEL_LOCKS_RECT[1] = (270, 180)
LEVEL_LOCKS_RECT[2] = (440, 180)
LEVEL_LOCKS_RECT[3] = (600, 180)
LEVEL_LOCKS_RECT[4] = (760, 180)
init_loading('loading assets', 5, True)