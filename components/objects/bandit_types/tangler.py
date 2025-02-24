import math
from random import randint

import pygame as pg

from assets import BULLET_CACHE
from components.hazzards.rope import Rope
from components.objects.bandit_model import BanditModel

from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.move_range = 600
        self.base_drop_chances = {'power_up': 15, 'item': 4000, 'brick': 40}
        self.points_value = 30
        self.destined_velocity = 3
        self.move_interval_base = [40, 120]
        self.can_shoot = False

        self.rope = BULLET_CACHE['rope'].copy()
        self.rope = pg.transform.scale(self.rope, (80, 80))
        self.rope.fill(colors.saddle_brown, special_flags=pg.BLEND_RGBA_MULT)
        self.rope_rect = self.rope.get_rect()

        self.rope_enabled = True
        self.can_shoot_rope = False
        self.rope_distance = 280
        self.rope_thickness = 12
        self.rope_tick = 0
        self.rope_interval = randint(50, 100)
        self.rope_direction = (0, 0)
        self.rope_length = 0
        self.rope_lifetick = 30

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        super().spawn(position, velocity, owner)
        self.can_shoot = False
        self.rope_enabled = True
        self.can_shoot_rope = False
        self.rope_tick = 0
        self.rope_interval = randint(50, 100)

    def shoot_rope(self, game):
        new_size = (self.rope_length, self.rope_thickness)
        new_pos = (self.rect.centerx + min(max(self.rope_direction[0], -20), 20),
                   self.rect.centery + min(max(self.rope_direction[1] , -20), 20))

        new_rope = Rope(game, new_pos, self.rope_direction, new_size, self)
        new_rope.set_lifetick(self.rope_lifetick)
        game.level.objects.append(new_rope)

        self.rope_enabled = False
        self.can_shoot_rope = False
        self.rope_tick = 0
        self.rope_interval = randint(50, 100)

    def on_rope_hit(self):
        self.rope_enabled = False
        self.can_shoot = True

    def check_rope(self, player):
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2) * 1.25
        return magnitude, (direction_x, direction_y), player
    def update(self, game):
        super().update(game)
        self.rope_rect.center = self.rect.center
        self.rope_tick += 1

        if self.rope_tick > self.rope_lifetick and not self.can_shoot:
            self.rope_enabled = True

        if self.rope_enabled and not self.can_shoot_rope and self.rope_tick > self.rope_interval:
            distance, direction, target = self.check_rope(game.player_1)
            if game.player_2 and self.check_rope(game.player_2)[0] > distance:
                distance, direction, target = self.check_rope(game.player_2)

            if self.rope_distance >= distance > 0 and not target.stuck:
                self.can_shoot_rope = True
                self.rope_direction = direction
                self.rope_length = distance
                self.rope_tick = 0

        if self.can_shoot_rope and self.rope_tick > 40:
            self.can_move = True
            self.shoot_rope(game)
            self.rope_tick = 0
            self.rope_interval = randint(50, 100)
            self.color = self.config['color']
            self.set_color()
        elif self.can_shoot_rope and self.push_velocity == (0, 0):
            self.can_move = False

            if self.tick % 6 == 0:
                if self.color == self.config['color']:
                    self.color = colors.bright_yellow
                    self.set_color()
                else:
                    self.color = self.config['color']
                    self.set_color()
        else:
            self.can_move = True

    def draw(self, game):
        super().draw(game)

        if self.visible and self.rope_enabled:
            game.screen.blit(self.rope, self.rope_rect)