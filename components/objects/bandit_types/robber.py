import math
from random import choice, randint

from components.objects.bandit_model import BanditModel

from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.can_shoot = True
        self.base_shoot_interval = 200
        self.base_drop_chances = {'power_up': 80, 'item': 80, 'brick': 80}
        self.base_health = 1
        self.points_value = 80
        self.move_interval_base = [100, 300]
        self.sprite.set_alpha(60)
        self.despawn_speed = 2

        self.stealing_target = None
        self.can_steal = False
        self.steal_tick = 0
        self.steal_interval = randint(40, 70)
        self.push_interval = 25

    def kill(self):
        super().kill()
        if self.stealing_target:
            self.stealing_target.stolen = False
            self.stealing_target.targeted_to_steal = False

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        super().spawn(position, velocity, owner)
        self.stealing_target = None
        self.can_steal = False
        self.can_push = True
        self.despawn_time = 20
        self.steal_tick = 0
        self.steal_interval = randint(100, 160)

    def get_steal_target(self, instance_list):
        if self.stealing_target:
            self.stealing_target.stolen = False

        if len(instance_list) > 0:
            choosen_target = choice(instance_list)
            if (not choosen_target.stolen and not choosen_target.targeted_to_steal
                    and choosen_target.is_placed):
                self.stealing_target = choice(instance_list)
                self.stealing_target.targeted_to_steal = True

    def is_close_enough(self):
        if self.stealing_target:
            direction_x = self.stealing_target.rect.centerx - self.rect.centerx
            direction_y = self.stealing_target.rect.centery - self.rect.centery
            magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
            return magnitude < 5

    def push(self, other_object):
        super().push(other_object)
        self.push_velocity = (self.push_velocity[0] // 1.7, self.push_velocity[1] // 1.7)

    def check_target_steal(self, game):
        if self.is_close_enough():
            self.steal_tick += 1

            if self.steal_tick > self.steal_interval:
                self.can_steal = True
                game.sound.play_sfx('remove')

    def update(self, game):
        super().update(game)

        if not self.despawning and not self.stealing_target:
            self.can_shoot = True
            self.get_steal_target(game.level.gadgets)
        elif self.stealing_target and not self.can_steal:
            self.max_magnitude, self.min_magnitude = 9999, 0
            self.check_target_steal(game)
            self.can_shoot = False

            if not self.is_close_enough():
                self.follow(self.stealing_target.rect)
                self.follow_strength = 4
            elif self.push_velocity == (0, 0):
                self.rect.center = self.stealing_target.rect.center

        if self.can_steal and self.stealing_target:
            self.stealing_target.stolen = True
            self.stealing_target.rect.center = self.rect.midtop
            self.despawn_time = 0

        if self.despawning and self.is_offscreen(game):
            self.kill()

            if self.stealing_target:
                self.stealing_target.kill()

