"""
Module for storing configuration constants and settings for the components.

This module contains variables related to screen configuration, game logic configuration,
components constants, and ui_sprites-related configurations.
It also stores the data and achievements format.
"""

from utils.colors import Colors
colors = Colors()

# Template for player data,
DATA_FORMAT = {
    "total_score": 0,
    "accumulated_score": 0,
    "victories": 0,
    "defeats": 0,

    "terrain_destroyed": 0,
    "blocks_destroyed": 0,
    "blocks_restored": 0,

    "p1_stats": {
        "bullets_reflected": 0,
        "bandits_killed": 0,
        "bandits_pushed": 0,
        "items_collected": 0,
        "powerups_collected": 0,
        "bandit_contacts": 0,
        "bullets_shot": 0,
        "damaged": 0,
    },
    "p2_stats": {
        "bullets_reflected": 0,
        "bandits_killed": 0,
        "bandits_pushed": 0,
        "items_collected": 0,
        "powerups_collected": 0,
        "bandit_contacts": 0,
        "bullets_shot": 0,
        "damaged": 0,
    },

    "level1": {
        "unlocked": True,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    },
    "level2": {
        "unlocked": False,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    },
    "level3": {
        "unlocked": False,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    },
    "level4": {
        "unlocked": False,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    },
    "level5": {
        "unlocked": False,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    },

    "achievements": {
        "defeat_A": False,
        "defeat_B": False,
        "defeat_C": False,
        "victory_A": False,
        "victory_B": False,
        "victory_C": False,
        "bandits_killed_A": False,
        "bandits_killed_C": False,
        "bandits_killed_B": False,
        "bandits_pushed": False,
        "bricks_collected": False,
        "terrain_destroyed": False,
        "damaged_A": False,
        "damaged_B": False,
        "loot": False,
        "boost": False,
        "contact": False,
        "score_A": False,
        "score_B": False,
        "score_C": False,
        "finish_story": False,
        "lucky_statue": False
    }
}


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

# COLLECTIBLE OBJECTS CONFIGURATION:
# index[0] = object name
# index[1] = the weight chance for rarity
# index[2] = max amount of times that it stacks when collected multiple times
# index[3] = points rewarded if you cannot collect it
POWER_UPS = {
    'shield_size': ['shield_size', 50, 3, 100],
    'bullet_size': ['bullet_size', 50, 3, 100],
    'auto_shoot': ['auto_shoot', 50, 3, 100],
    'extra_block': ['extra_block', 50, 3, 100],
    'ghost_fury': ['ghost_fury', 50, 2, 100],

    'magnet': ['magnet', 30, 2, 150],
    'recovery': ['recovery', 30, 3, 150],

    'extra_reflect': ['extra_reflect', 20, 2, 200],
    'space_shield': ['space_shield', 10, 1, 300],
}

ITEMS = {
    'bomb': ['bomb', 50, 0, 0],
    'shield': ['shield', 40, 3, 30],
    'turret_shooter': ['turret_shooter', 30, 5, 100],
    'turret_shield': ['turret_shield', 30, 5, 100],
    'bot_shooter': ['bot_shooter', 20, 5, 100],
    'healing_ufo': ['healing_ufo', 20, 1, 100],
    'gift_bomb': ['gift_bomb', 0.3, 0, 0],
}

BRICKS = {
    # bricks do not include max stacks or points rewards, only name and chance.
    'brick': ['brick', 70],
    'double_brick': ['double_brick', 30],
    'brick_pile': ['brick_pile', 10],
}

# Level configuration
LEVEL_CONFIG = [
    {  # ===== LEVEL 0 ( TUTORIAL ) CONFIGURATIONS =====
        "background": (25, 20, 30),
        "spawn_types":
            [
                # [0] = Name, [1] = Chance, [2] = Spawn only on Ambush, [3] = Ambush chance increment
                ["basic", 100, False, 0]
            ],
        "terrain_noise": 2,     # Strength of terrain count that attempts to spawn, multiplier.
        "terrain_area_reduction": 3,    # Size of spacing area between terrain, multiplied by the terrain size.

        "round_time": 9999999999,
        "max_bandits": 0,
        "max_spawn_count": 0,
        "bandit_spawnrate": 300,
        "bandit_spawn_multi": [1, 2],   # Multiplier for bandits spawned for before and after ambush starts.
        "difficulty_time": 15,  # Interval in seconds that difficulty will increase.
        "can_spawn_early": True,    # If bandits can spawn before the starting messages are gone.

    },
    { # ===== LEVEL 1 ( DESERT ) CONFIGURATIONS =====
        "background": (50, 30, 0),
        "spawn_types":
            [
                ["basic", 80, False, -15],
                ["skilled", 20, False, 10],
                ["bomber", 18, True, 0],
                ["hitman", 10, True, 0],
            ],
        "terrain_noise": 10,
        "terrain_area_reduction": 1,

        "round_time": 300,
        "max_bandits": 2,
        "max_spawn_count": 2,
        "bandit_spawnrate": 300,
        "bandit_spawn_multi": [1, 2],
        "difficulty_time": 15,
        "spawn_start_time": 5,
    },
    { # ===== LEVEL 2 ( SALOON ) CONFIGURATIONS =====
        "background": (60, 40, 35),
        "spawn_types":
            [
                ["basic", 80, False, -15],
                ["dicer", 15, False, 5],
                ["shielded", 15, False, 5],
                ["hitman", 10, True, 0],
                ["tipsy", 25, True, 0],
            ],
        "terrain_noise": 4,
        "terrain_area_reduction": 1.2,

        "round_time": 300,
        "max_bandits": 3,
        "max_spawn_count": 2,
        "bandit_spawnrate": 240,
        "bandit_spawn_multi": [1, 2],
        "difficulty_time": 15,
        "spawn_start_time": 3,

    },
    { # ===== LEVEL 3 ( BARREN ) CONFIGURATIONS =====
        "background": (30, 25, 20),
        "spawn_types":
            [
                ["basic", 30, False, -20],
                ["skilled", 50, False, -10],
                ["boomstick", 30, False, 10],
                ["bomber", 5, False, 25],
                ["tangler", 5, False, 25],
                ["hitman", 10, True, 0],
            ],
        "terrain_noise": 10,
        "terrain_area_reduction": 2,

        "round_time": 240,
        "max_bandits": 4,
        "max_spawn_count": 1,
        "bandit_spawnrate": 200,
        "bandit_spawn_multi": [1, 3],
        "difficulty_time": 15,
        "spawn_start_time": 3,
    }

]

ACHIEVEMENT_LIST = {
    # [1] = Name, [2] = Hint to unlock, [3] = Description (when unlocked)

    "defeat_A": [
        "Caged Up",
        "Get captured by the bandits for the first time",
        "Don't give up! These bandits got nothing on you!"
    ],
    "defeat_B": [
        "Many to Come",
        "Get captured 5 times by the bandits",
        "This just means you're learning! Hopefully..."
    ],
    "defeat_C": [
        "Public enemy",
        "Get captured 25 times by the bandits",
        "These bandits sure hate your guts, maybe talk things out?"
    ],
    "victory_A": [
        "Space Calls!",
        "Escape the bandits for the first time",
        "Flying back to space to have an awesome trip through the galaxy!"
    ],
    "victory_B": [
        "Professional Survivor",
        "Escape the bandits 5 times",
        "Ever thought about writing a wild west survival series? For aliens, of course."
    ],
    "victory_C": [
        "Local Hotspot",
        "Escape the bandits 25 times",
        "You must really like to orbit this planet specifically to keep falling here, huh?"
    ],
    "bandits_killed_A": [
        "Right Back At Ya!",
        "Kill 50 bandits with their own bullets",
        "Nothing feels better than giving shooters a taste of their own medicine!"
    ],
    "bandits_killed_B": [
        "Bandit Massacre",
        "Kill 250 bandits",
        "That tastes a bit more like their own medicine, don't you think?"
    ],
    "bandits_killed_C": [
        "Bandit Genocide",
        "Kill 1000 bandits",
        "Your Level Of Violence is off the charts!"
    ],
    "bandits_pushed": [
        "Back Off!",
        "Push back 100 bandits",
        "It's just more practical this way."
    ],
    "bricks_collected": [
        "Bob the Alien",
        "Restore 50 UFO parts with picked up bricks",
        "That thing won't be flying broken!"
    ],
    "terrain_destroyed": [
        "Enviroment Hazzard",
        "Destroy 50 of the decorative terrain with explosions",
        "And somehow, they can drop bricks. Still not a good practice!"
    ],
    "damaged_A": [
        "Ouch!",
        "Get turned into a ghost 25 times",
        "Come on, it's not THAT bad..."
    ],
    "damaged_B": [
        "Owiee!!!",
        "Get turned into a ghost 100 times",
        "Okok, stop!! I was joking! It does hurt!"
    ],
    "loot": [
        "Loot! Loot!",
        "Collect 100 of any item",
        "Is it really a western game without the primal urge to collect everything on your path?"
    ],
    "boost": [
        "Superpowered",
        "Get 25 of any power ups",
        "Soon enough you might solo goku! (Lies, nobody solos goku)"
    ],
    "contact": [
        "Friendly Foe",
        "Touch 50 bandits, ghost form counts",
        "Come on! Give them a high five! Wait you don't have hands... Oh......."
    ],
    "score_A": [
        "Beginner",
        "Get 10000 total score",
        "Well, surely you can get it higher than that!"
    ],
    "score_B": [
        "Skilled One",
        "Get 25000 total score",
        "Now THAT'S more like it!"
    ],
    "score_C": [
        "Gamer",
        "Get 50000 total score",
        "You have mastered the ways of the gamer, I salute you."
    ],
    "finish_story": [
        "The End",
        "Defeat the Chief of the Bandits",
        'I guess this truly was a raid of the western...'
    ],
    "lucky_statue": [
        "Odd Statue",
        "Find the rare snake statue in any level",
        "Break it? Use it? Nobody knows what this BARREN sculpture is for..."
    ],
    "secret_boss": [
        "The Golden One",
        "This achievement is a secret...",
        "Quite a surprise! I wonder if you figured this by youself!"
    ],
}