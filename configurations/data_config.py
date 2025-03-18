from configurations.achievements_config import ACHIEVEMENT_LIST
from constants import LEVEL_COUNT

# Configuration for player data template
DATA_FORMAT = {
    "total_score": 0,
    "accumulated_score": 0,

    "terrain_destroyed": 0,
    "blocks_destroyed": 0,
    "blocks_restored": 0,
    "gadgets_placed": 0,
}

for level in LEVEL_COUNT:
    DATA_FORMAT[f'level{level}'] = {
        "unlocked": False,
        "wins": 0,
        "defeats": 0,
        "best_score": 0,
        "p1_score": 0,
        "p2_score": 0,
    }

first_lv = DATA_FORMAT.get(f'level{LEVEL_COUNT[0]}')
first_lv['unlocked'] = True

for player in range(1, 3):
    DATA_FORMAT[f'p{player}_stats'] = {
        "bullets_reflected": 0,
        "bandits_killed": 0,
        "bandits_pushed": 0,
        "items_collected": 0,
        "powerups_collected": 0,
        "bandit_contacts": 0,
        "bullets_shot": 0,
        "damaged": 0,
    }

DATA_FORMAT['achievements'] = {}
for achievement in ACHIEVEMENT_LIST.keys():
    DATA_FORMAT['achievements'][achievement] = False