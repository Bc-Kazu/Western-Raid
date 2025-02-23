from components.hazzards.explosion import Explosion
from components.objects.bandit_model import BanditModel

from random import randint
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.can_shoot = False
        self.base_drop_chances = {'power_up': 10, 'item': 40, 'brick': 0}
        self.points_value = 40
        self.move_interval_base = [10, 60]

        self.explode = [False, 0, 90, False, False]
        self.random_near_ufo = randint(60, 120)

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.random_near_ufo = randint(60, 120)
        self.explode = [False, 0, 90, False, False]
        super().spawn(position, velocity, owner)
        super().set_color()

    def update(self, game):
        super().update(game)

        if not self.despawning:
            self.max_magnitude, self.min_magnitude = 9999, self.random_near_ufo
            self.follow(game.ufo.rect)

        # System to handle the entire process of bandit causing explosion
        self.explode[1] += 1

        if 6 <= self.lifetime < 8:
            if self.explode[1] >= 8:
                self.explode[1] = 0
                self.explode[3] = not self.explode[3]

                if self.explode[3]:
                    self.set_color(colors.red)
                else:
                    self.set_color(colors.light_orange)
        elif self.lifetime >= 8 and not self.explode[0]:  # Creating the explosion
            self.kill()
            self.explode[0] = False
            new_explosion = Explosion(game, self.rect.center, self.size[1] * 2)
            game.level.objects.append(new_explosion)