from random import randint, choice
from components.objects.bandit_model import BanditModel
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.bullet_type = 'card'
        self.base_shoot_interval = 200
        self.move_range = 500
        self.drop_chances = {'power_up': 50, 'item': 30, 'brick': 20}
        self.points_value = 50
        self.move_interval_base = [100, 500]