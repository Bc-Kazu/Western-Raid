from random import randint, choice
from components.objects.bandit_model import BanditModel
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.bullet_type = 'card'
        self.base_shoot_interval = 140
        self.move_range = 500
        self.base_drop_chances = {'power_up': 40, 'item': 15, 'brick': 20}
        self.points_value = 50
        self.move_interval_base = [100, 500]

        self.protect_cards_shot = 0
        self.protect_cards_max = 3

    def get_target(self, game):
        target = choice(game.level.bandits)
        if target == self:
            super().get_target(game)
            return

        self.target = target

    def update(self, game):
        super().update(game)

        if self.last_bullet_buff == 'protection':
            self.protect_cards_shot += 1
            if self.protect_cards_shot < self.protect_cards_max:
                self.shoot(game, self.target)
        else:
            self.protect_cards_shot = 0

