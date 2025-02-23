from components.objects.bandit_model import BanditModel

from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.bullet_type = 'dynamite'
        self.base_shoot_interval = 200
        self.move_range = 350
        self.base_drop_chances = {'power_up': 12, 'item': 70, 'brick': 10}
        self.points_value = 40
        self.move_interval_base = [70, 240]
        self.bullet_speed = 3