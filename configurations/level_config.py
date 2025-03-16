# Level configuration
LEVEL_CONFIG = [
    {  # ===== LEVEL 0 ( TUTORIAL ) CONFIGURATIONS =====
        "background": (25, 20, 30),
        "music": 'sandwreck',
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
        "music": 'sandwreck',
        "spawn_types":
            [
                ["basic", 80, False, -15],
                ["skilled", 20, False, 10],
                ["tangler", 20, True, 0],
                ["bomber", 20, True, 0],
                ["hitman", 10, True, 0],
                ["robber", 5, True, 0],
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
        "background": (80, 58, 40),
        "music": 'tabletoss',
        "spawn_types":
            [
                ["basic", 80, False, -15],
                ["dicer", 15, False, 5],
                ["shielded", 15, False, 5],
                ["hitman", 10, True, 0],
                ["tipsy", 25, True, 0],
                ["robber", 5, True, 0],
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
        "music": 'sandwreck',
        "spawn_types":
            [
                ["basic", 30, False, -20],
                ["skilled", 50, False, -10],
                ["boomstick", 30, False, 10],
                ["bomber", 5, False, 25],
                ["tangler", 5, False, 25],
                ["hitman", 10, True, 0],
                ["robber", 5, True, 0],
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