# COLLECTIBLE OBJECTS CONFIGURATION:
# index[0] = object name
# index[1] = the weight chance for rarity
# index[2] = max amount of times that it stacks when collected multiple times
# index[3] = points rewarded if you cannot collect it
POWER_UPS = {
    'shield_size': ['shield_size', 50, 3, 100],
    'bullet_size': ['bullet_size', 50, 3, 100],
    'extra_block': ['extra_block', 50, 3, 100],

    'auto_shoot': ['auto_shoot', 40, 3, 100],
    'recovery': ['recovery', 40, 3, 100],

    'extra_reflect': ['extra_reflect', 30, 3, 150],
    'magnet': ['magnet', 30, 2, 150],
    'ghost_fury': ['ghost_fury', 30, 2, 150],

    'space_shield': ['space_shield', 15, 1, 300],
}

ITEMS = {
    'shield': ['shield', 60, 3, 50],
    'bomb': ['bomb', 55, 0, 0],
    'turret_shooter': ['turret_shooter', 25, 5, 100],
    'shield_pylon': ['shield_pylon', 25, 3, 100],
    'bot_shooter': ['bot_shooter', 20, 5, 100],
    'auto_heal': ['auto_heal', 15, 1, 150],
    'gift_bomb': ['gift_bomb', 0.3, 0, 0],
}

BRICKS = {
    # bricks do not include max stacks or points rewards, only name and chance.
    'brick': ['brick', 70],
    'double_brick': ['double_brick', 30],
    'brick_pile': ['brick_pile', 10],
}