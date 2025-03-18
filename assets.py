"""
Module for loading and configuring components assets.

This module handles the initialization of fonts and the loading and transformation
of image resources. It centralizes asset management to keep the main code clean.
"""
import sys

import pygame as pg
import os
import inspect
from random import choice

from utils.text import Text
from utils.colors import Colors
from constants import LEVEL_COUNT, SCREEN_WIDTH, SCREEN_HEIGHT
from configurations.pickup_config import POWER_UPS, ITEMS, BRICKS
from configurations.caption_config import RANDOM_INIT_CAPTION

# Get the current local date and time
colors = Colors()
pg.init()

# Temporary scren values, do not use these in other files
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PYGAME_IMAGE = pg.image.load(f'assets/pygame.png').convert_alpha()
PYGAME_IMAGE = pg.transform.scale(PYGAME_IMAGE, (150, 150))
PYGAME_IMAGE_RECT = PYGAME_IMAGE.get_rect()
PYGAME_IMAGE_RECT.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

pg.display.set_caption(choice(RANDOM_INIT_CAPTION))
pg.display.set_icon(PYGAME_IMAGE)

def get_line_number():
    """Returns the current line number in the script."""
    return inspect.currentframe().f_back.f_lineno

# Font configuration
SMALL_FONT = pg.font.Font("assets/retro_font.ttf", 16)
TEXT_FONT = pg.font.Font("assets/retro_font.ttf", 24)
NORMAL_FONT = pg.font.Font("assets/retro_font.ttf", 40)
TITLE_FONT = pg.font.Font("assets/retro_font.ttf", 72)

PYGAME_HAPPY_IMAGE = pg.image.load(f'assets/pygame_happy.png').convert_alpha()
PYGAME_HAPPY_IMAGE = pg.transform.scale(PYGAME_HAPPY_IMAGE, (150, 150))

POWERED_BY_TEXT = Text('POWERED BY', (SCREEN_WIDTH // 2, PYGAME_IMAGE_RECT.top - 10),
                         TEXT_FONT, colors.pale_yellow)
PYGAME_TEXT = Text('PYGAME', (SCREEN_WIDTH // 2,PYGAME_IMAGE_RECT.bottom),
                         NORMAL_FONT, colors.light_yellow)
PYGAME_TEXT.set_background(True)
INIT_LOADING_TEXT = Text('LOADING GAME...', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3),
                         TEXT_FONT, colors.light_grey)
INIT_LOADING_DESC = Text('This game automatically saves your data!',
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.05), TEXT_FONT, colors.grey)
BLACK_SCREEN = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
BLACK_SCREEN.fill(colors.black)

loading_progress = 0
def sfx(name):
    sound = pg.mixer.Sound(f'assets/SFX/{name}.wav')
    sound.set_volume(0.3)
    sound.play()

def init_loading(string, progress=None, reset_progress=False):
    global loading_progress
    pg.event.pump()
    loading_progress += progress if progress else 0
    # string = f'{string} ({loading_progress})' if progress else f'{string}'

    if loading_progress < 100:
        new_alpha = BLACK_SCREEN.get_alpha() - 5
        if new_alpha < 0:
            new_alpha = 0
        BLACK_SCREEN.set_alpha(new_alpha)
    elif loading_progress < 120:
        BLACK_SCREEN.set_alpha(0)

    if loading_progress > 240:
        new_alpha = BLACK_SCREEN.get_alpha() + 3
        if new_alpha > 255:
            new_alpha = 255
        BLACK_SCREEN.set_alpha(new_alpha)

    SCREEN.fill((0, 0, 0))
    if loading_progress == 220:
        sfx('points_extra')
        INIT_LOADING_TEXT.set_text('LOADED!')
        pg.display.set_icon(PYGAME_HAPPY_IMAGE)
    if loading_progress < 220:
        SCREEN.blit(PYGAME_IMAGE, PYGAME_IMAGE_RECT)
    else:
        SCREEN.blit(PYGAME_HAPPY_IMAGE, PYGAME_IMAGE_RECT)

    # INIT_LOADING_DESC.set_text(string)

    INIT_LOADING_DESC.draw(None, SCREEN)
    INIT_LOADING_TEXT.draw(None, SCREEN)
    POWERED_BY_TEXT.draw(None, SCREEN)
    PYGAME_TEXT.draw(None, SCREEN)
    SCREEN.blit(BLACK_SCREEN, (0, 0))
    pg.display.flip()

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # if reset_progress:
        # loading_progress = 0

supported_formats = ["bmp", "png", "jpg", "jpeg", "gif", "tga", "webp"]
def load_cache(folder_path):
    """Loads all images from a folder into the image cache dictionary."""
    cache = {}
    for filename in os.listdir(folder_path):
        if "." in filename and filename.rsplit(".", 1)[1] in supported_formats:
            image_name = filename.rsplit(".", 1)[0]
            cache[image_name] = pg.image.load(os.path.join(folder_path, filename)).convert_alpha()
            init_loading('loading assets', 1)
    return cache

# Preloading all images that are added/removed through the game
BANDIT_CACHE = load_cache("assets/bandit_sprites")
BULLET_CACHE = load_cache("assets/bullet_sprites")
DECORATION_CACHE = load_cache("assets/decoration_sprites")
ITEM_CACHE = load_cache("assets/item_sprites")
TERRAIN_CACHE = load_cache("assets/terrain_sprites")
UI_CACHE = load_cache("assets/ui_sprites")
BLOCK_CACHE = load_cache("assets/block_sprites")
GADGET_CACHE = load_cache("assets/gadget_sprites")
UFO_CACHE = load_cache("assets/ufo_sprites")
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

init_loading('loading assets', 5)

UFO_CONFIG = {
    'name': 'spaceship',
    'type': 'ufo',
    'size': (180, 180),
    'color': colors.light_blue,
    'image': UFO_CACHE['ufo1'].copy()
}

GADGET_CONFIG = {
    'turret_shooter': {'name': 'turret_shooter', 'type': 'gadget', 'size': (60, 60),
        'image': GADGET_CACHE['turret_shooter'].copy(), 'can_hold': True},
    'turret_shield': {'name': 'turret_shield', 'type': 'gadget', 'size': (60, 60),
                       'image': GADGET_CACHE['turret_shield'].copy(), 'can_hold': True},
    'bot_shooter': {'name': 'bot_shooter', 'type': 'gadget', 'size': (40, 40),
                       'image': GADGET_CACHE['bot_shooter'].copy(), 'can_hold': False},
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
    "robber": {'name': 'robber', 'type': 'enemy', 'size': (60, 60),
              'color': colors.white, 'image': BANDIT_CACHE['robber'].copy()},
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
init_loading('loading assets', 2)

WASD_CONTROLS_B = pg.image.load('assets/ui_sprites/WASD.png').convert_alpha()
ARROWS_CONTROLS_B = pg.image.load('assets/ui_sprites/ARROWS.png').convert_alpha()
WASD_CONTROLS_B = pg.transform.scale(WASD_CONTROLS_B, (55, 36))
ARROWS_CONTROLS_B = pg.transform.scale(ARROWS_CONTROLS_B, (55, 36))
WASD_RECT_B = WASD_CONTROLS_B.get_rect()
ARROWS_RECT_B = ARROWS_CONTROLS_B.get_rect()
init_loading('loading assets', 6)

# Creating level icons, frames and locks
LEVEL_ICONS = [None,
    TERRAIN_CACHE['cactus1'].copy(),
    TERRAIN_CACHE['arcade_machine'].copy(),
    TERRAIN_CACHE['fossil2'].copy(),
    UI_CACHE['question'].copy(),
    UI_CACHE['question'].copy()
]
init_loading('loading assets', 5)

ICON_COLORS = [None, (60, 160, 90), (155, 130, 80), (150, 150, 150), (100, 0, 0), (100, 0, 0)]
LEVEL_FRAMES = {}
LEVEL_FRAMES_RECT = {}
LEVEL_ICONS_RECT = {}
LEVEL_LOCKS = {}
LEVEL_LOCKS_RECT = {}

for level in LEVEL_COUNT:
    base_rect = (110, 180)
    offset = 160 * (level - 1)
    LEVEL_ICONS[level] = pg.transform.scale(LEVEL_ICONS[level], (80, 80))
    LEVEL_ICONS[level].fill(ICON_COLORS[level], special_flags=pg.BLEND_RGBA_MULT)
    LEVEL_ICONS_RECT[level] = (base_rect[0] + offset, base_rect[1])

    LEVEL_FRAMES[level] = UI_FRAME.copy()
    LEVEL_FRAMES_RECT[level] = (base_rect[0] - 10 + offset, base_rect[1] - 10)

    LEVEL_LOCKS[level] = pg.transform.scale(UI_CACHE['locked'].copy(), (80, 80))
    LEVEL_LOCKS_RECT[level] = (base_rect[0] + offset, base_rect[1])
    init_loading('loading assets', 3)

init_loading('loading assets', 10, True)