from components.hazzards.explosion import Explosion
from components.objects.bandit_model import BanditModel

from random import randint
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.can_shoot = False
        self.base_drop_chances = {'power_up': 15, 'item': 60, 'brick': 0}
        self.points_value = 40
        self.move_interval_base = [10, 60]
        self.random_near_ufo = randint(60, 120)
        self.push_weight = 1.5
        self.push_interval = 12

        # Values for explosion process
        self.explosion_time = 6
        self.exploded = False
        self.explode_switch = False
        self.switch_tick = 0
        self.switch_interval = 16

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.random_near_ufo = randint(60, 120)
        super().spawn(position, velocity, owner)
        super().set_color()
        self.move_tick = self.move_interval
        self.spawn_grace = False

        self.explosion_time = 6
        self.exploded = False
        self.explode_switch = False
        self.switch_interval = 16

    def update(self, game):
        super().update(game)

        if not self.despawning:
            self.max_magnitude, self.min_magnitude = 9999, self.random_near_ufo
            self.follow(game.ufo.rect)

        self.explode_process(game)


    # System to handle the entire process of bandit causing explosion
    def explode_process(self, game):
        if self.explosion_time >  self.lifetime >= self.explosion_time - 2:
            self.switch_tick += 1

            if self.switch_tick > self.switch_interval:
                self.switch_tick = 0
                self.explode_switch = not self.explode_switch
                self.switch_interval = (self.switch_interval - 2) if self.switch_interval > 4 else 4
                self.set_color(colors.red if self.explode_switch else colors.orange)
        elif self.lifetime >= self.explosion_time and not self.exploded:  # Creating the explosion
            self.kill()
            self.exploded = False
            explosion_size = (self.size[0] * 2, self.size[1] * 2)
            new_explosion = Explosion(game, self.rect.center, explosion_size)
            game.level.objects.append(new_explosion)
