from random import randint
from components.objects.bandit_model import BanditModel
from components.hazzards.poison import Poison
from assets import BULLET_CACHE

import pygame as pg

from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.can_shoot = False
        self.move_range = 1000
        self.points_value = 25
        self.move_interval_base = [60, 180]
        self.last_side = [self.size[0] - 20, 0]
        self.destined_velocity = 3

        self.puddle_color = colors.moss_green
        self.bottle = BULLET_CACHE['bottle'].copy()
        self.bottle = pg.transform.scale(self.bottle, (80, 80))
        self.bottle.fill(self.puddle_color, special_flags=pg.BLEND_RGBA_MULT)
        self.bottle_rect = self.bottle.get_rect()
        self.random_drink_time = randint(4, 7)
        self.drink_anim = [False, 0 , 120, False,  0, 60, 0, 40, False]

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.bottle = BULLET_CACHE['bottle'].copy()
        self.bottle = pg.transform.scale(self.bottle, (80, 80))
        self.bottle.fill(self.puddle_color, special_flags=pg.BLEND_RGBA_MULT)
        self.bottle_rect = self.bottle.get_rect()
        self.drink_anim = [False, 0 , 120, False,  0, 60, 0, 40, False]
        self.random_drink_time = randint(4, 7)
        self.reset_sprite()

        super().spawn(position, velocity, owner)

    # Handling totally legal and PG friendly drink bottle system for this bandit
    def update(self, game):
        super().update(game)
        # Choosing the side position and flipping bottle depending on position
        left_distance = [[self.size[0] - 20, 0], 0 + self.rect.x, -90]
        right_distance = [[-self.size[0] + 20, 0], game.screen_width - self.rect.x, 90]
        smallest_x = min(left_distance[1], right_distance[1])

        side_goal = left_distance if smallest_x == left_distance[1] else right_distance

        if self.last_side != side_goal[0]:
            self.bottle = pg.transform.flip(self.bottle, True, False)

        self.bottle_rect.center = self.rect.center
        self.bottle_rect.x += side_goal[0][0]
        self.bottle_rect.y += side_goal[0][1]
        self.last_side = side_goal[0]

        # Drink puddle animation and spawning process
        if self.lifetime > self.random_drink_time:
            self.can_move = False

            if not self.drink_anim[0]:
                self.bottle = pg.transform.rotate(self.bottle, side_goal[-1])
                self.drink_anim[0] = True
            elif self.drink_anim[1] < self.drink_anim[2]:
                self.drink_anim[1] += 1
            elif self.drink_anim[4] == 0:
                self.bottle = pg.transform.rotate(self.bottle, -side_goal[-1])
                self.drink_anim[4] += 1
            elif self.drink_anim[4] < self.drink_anim[5]:
                self.drink_anim[4] += 1
            elif not self.drink_anim[3]:
                self.sprite = pg.transform.rotate(self.sprite, -side_goal[-1])
                self.drink_anim[3] = True
                self.active = False
                self.can_collide = False
            elif self.drink_anim[6] < self.drink_anim[7]:
                self.drink_anim[6] += 1
            elif not self.drink_anim[8]:
                self.drink_anim[8] = True

                # Spawning the weird liquid thingy after the animation ends
                puddle = Poison(self.rect.center, self.size[1], self.puddle_color)
                game.level.objects.append(puddle)

    def draw(self, game):
        super().draw(game)

        if not self.drink_anim[3]:
            game.screen.blit(self.bottle, self.bottle_rect)