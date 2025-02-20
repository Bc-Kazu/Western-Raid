from random import randint, choice
from components.objects.bandit_model import BanditModel
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.base_shoot_interval = 240
        self.move_range = 800
        self.drop_chances = {'power_up': 20, 'item': 60, 'brick': 100}
        self.points_value = 50
        self.move_interval_base = [90, 300]
        self.can_push = False
        self.bullet_speed = 7
        self.bullet_type = 'card'