"""
Module for storing configuration constants and settings for the components.

This module contains variables related to screen configuration, game logic configuration,
components constants, and ui_sprites-related configurations.
"""

from utils.colors import Colors
colors = Colors()

# Screen configuration
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620

# Level access configuration
LEVEL_COUNT = [1]
ALLOWED_LEVELS = [1, 2, 3]

# Basic color configuration
PLAYER_COLORS = [colors.bright_green, colors.bright_purple]
UFO_COLORS = [
    [   # Brick power 1
        colors.window_white,
        colors.window_white,
        colors.window_white,
        colors.ufo_bottom_1,
        colors.ufo_bottom_1,
    ],
    [   # Brick power 2
        colors.window_bright_yellow,
        colors.window_bright_yellow,
        colors.window_bright_yellow,
        colors.ufo_bottom_2,
        colors.ufo_bottom_2,
    ],
    [   # Brick power 3+
        colors.window_light_yellow,
        colors.window_light_yellow,
        colors.window_light_yellow,
        colors.ufo_bottom_3,
        colors.ufo_bottom_3,
    ],
]

# Making a custom breakout-style grid just for fun :)
BREAKOUT_SHAPE = [[1] * 14] * 8
BREAKOUT_COLORS = [
    [  # Brick power 1
        colors.red,
        colors.red,
        colors.orange,
        colors.orange,
        colors.green,
        colors.green,
        colors.yellow,
        colors.yellow,
    ],
    [  # Brick power 2
        colors.light_red,
        colors.light_red,
        colors.light_orange,
        colors.light_orange,
        colors.light_green,
        colors.light_green,
        colors.light_yellow,
        colors.light_yellow,
    ],
    [  # Brick power 3+
        colors.bright_red,
        colors.bright_red,
        colors.bright_orange,
        colors.bright_orange,
        colors.bright_green,
        colors.bright_green,
        colors.bright_yellow,
        colors.bright_yellow,
    ],
]

# More custom grids for the ufo yippiee (this is tower)
TOWER_SHAPE = [
            [1, -1, 1, -1, 1],
            [1, 1, 1, 1, 1],
               [1, 1, 1],
               [1, 0, 1],
               [1, 1, 1],
               [1, 1, 1],
              [1, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ]

TOWER_COLORS = [
    [  # Brick power 1
        colors.white,
        colors.white,
        colors.silver,
        colors.silver,
        colors.grey,
        colors.grey,
        colors.charcoal,
        colors.charcoal,
    ],
    [  # Brick power 2
        colors.bright_cyan,
        colors.bright_cyan,
        colors.sky_blue,
        colors.sky_blue,
        colors.azure,
        colors.azure,
        colors.navy,
        colors.navy,
    ],
    [  # Brick power 3+
        colors.bright_purple,
        colors.bright_purple,
        colors.pastel_purple,
        colors.pastel_purple,
        colors.magenta,
        colors.magenta,
        colors.indigo,
        colors.indigo,
    ],
]

# Constant variables
BASE_SHIELD_X = 130
BASE_SHIELD_Y = 20
SHIELD_DISTANCE = 70

BASE_PLAYER_SPEED = 4
BASE_ENEMY_SPEED = 2
MAX_BULLET_SPEED = 5