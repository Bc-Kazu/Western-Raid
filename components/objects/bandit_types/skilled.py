from components.objects.bandit_model import BanditModel
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.base_shoot_interval = 90
        self.move_range = 400
        self.base_drop_chances = {'power_up': 15, 'item': 30, 'brick': 60}
        self.points_value = 40
        self.bullet_speed = 5
        self.destined_velocity = 3
        self.move_interval_base = [120, 700]