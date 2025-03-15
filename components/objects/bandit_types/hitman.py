from random import randint, choice
from components.objects.bandit_model import BanditModel
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.base_shoot_interval = 180
        self.move_range = 500
        self.base_drop_chances = {'power_up': 40, 'item': 70, 'brick': 100}
        self.points_value = 80
        self.move_interval_base = [40, 200]
        self.destined_velocity = 4
        self.can_push = False
        self.bullet_speed = 7

    def get_random_destination(self, game):
        target = [game.player_1, game.player_2 if game.player_2 else game.player_1][randint(0, 1)]
        if target:
            new_x = target.rect.centerx
            new_y = target.rect.centery

            if new_x < self.rect.centerx:
                new_x += randint(50, 150)
            elif new_x > self.rect.centerx:
                new_x -= randint(50, 150)
            if new_y < self.rect.centery:
                new_y += randint(50, 150)
            elif new_y > self.rect.centery:
                new_y -= randint(50, 150)

            self.set_destination(new_x, new_y)
        else:
            super().get_random_destination(game)

    def get_target(self, game):
        if game.player_1:
            possible_targets = [game.player_1, game.player_2 if game.player_2 else game.player_1]
            target = possible_targets[randint(0, 1)]
            self.target = target
        else:
            super().get_target(game)

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        super().spawn(position, velocity, owner)
        self.move_interval = 0