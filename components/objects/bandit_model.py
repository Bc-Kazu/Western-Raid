from random import randint, choice
from components.game_object import GameObject

import math
import pygame as pg

from utils.colors import Colors
colors = Colors()

''' Superclass containing all of basic bandit configurations and functions '''
# Access each bandit type file to see their own settings, including specific functions.
class BanditModel(GameObject):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.offscreen_limit = 0
        self.max_lifetime = 30
        self.screen_limited = True
        self.can_push = True

        self.base_health = 1
        self.health = 1
        self.points_value = 20
        self.base_drop_chances = {'power_up': 10, 'item': 20, 'brick': 40}
        self.drop_chances = self.base_drop_chances
        self.spawn_grace = True

        # Movement settings
        self.move_range = 250
        self.move_interval = 120
        self.move_interval_base = [180, 900]
        self.move_interval_range = self.move_interval_base[:]
        self.move_tick = 0
        self.last_side = [self.size[0], 0]

        self.despawn_time = 20
        self.despawning = False
        self.active = True

        # Shooting settings
        self.can_shoot = True
        self.target = None
        self.bullet_type = 'bullet'
        self.bullet_speed = 4
        self.shoot_tick = 0
        self.base_shoot_interval = randint(110, 130)
        self.shoot_interval = self.base_shoot_interval

        # Special buff values
        self.shield_enabled = False

        protection_size = (int(self.size[0] * 1.2), int(self.size[1] * 1.2))
        self.protection = pg.Surface(protection_size, pg.SRCALPHA)
        self.protection.fill((80, 80, 255, 30))
        self.protection_rect = self.protection.get_rect()
        self.protection_hp = 0

        self.movement_surface = pg.Surface((self.move_range, self.move_range), pg.SRCALPHA)
        self.movement_surface.fill(colors.purple)
        self.movement_surface.set_alpha(50)
        self.movement_rect = pg.Rect(0, 0, self.move_range, self.move_range)

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        lower_size = (self.size[0] - 5, self.size[1] - 5)
        higher_size = (self.size[0] + 5, self.size[1] + 5)
        self.size = choice([lower_size, self.size, higher_size])
        self.move_interval_range = self.move_interval_base[:]
        self.health = self.base_health
        self.drop_chances = self.base_drop_chances
        self.target = None
        self.despawning = False
        self.move_interval = randint(40, 120)
        self.move_tick = 0
        self.shoot_tick = 0
        self.shoot_interval = self.base_shoot_interval
        self.spawn_grace = True

        self.movement_surface = pg.Surface((self.move_range, self.move_range), pg.SRCALPHA)
        self.movement_surface.fill(colors.purple)
        self.movement_surface.set_alpha(50)
        self.movement_rect = pg.Rect(0, 0, self.move_range, self.move_range)

        protection_size = (int(self.size[0] * 1.2), int(self.size[1] * 1.2))
        self.protection = pg.Surface(protection_size, pg.SRCALPHA)
        self.protection.fill((80, 80, 255, 30))
        self.protection_rect = self.protection.get_rect()
        self.protection_hp = 0

        super().spawn(position, velocity, owner)
        self.set_color()

    def get_drop(self):
        # Chance to give the bandit an item to drop at death
        if randint(0, self.drop_chances['power_up']) >= randint(0, 100):
            return 'power_up'
        elif randint(0, self.drop_chances['item']) >= randint(0, 100):
            return 'item'
        elif randint(0, self.drop_chances['brick']) >= randint(0, 100):
            return 'brick'
        else:
            return None

    def get_random_destination(self, game):
        # Finding a random target position while remaining bandit inside screen.
        new_x = randint(self.movement_rect.left, self.movement_rect.right)
        new_y = randint(self.movement_rect.top, self.movement_rect.bottom)
        if new_x < self.size[0] // 2:
            new_x = self.size[0] // 2
        elif new_x > game.screen_width - self.size[0] // 2:
            new_x = game.screen_width - self.size[0] // 2
        if new_y < self.size[1] // 2:
            new_y = self.size[1] // 2
        elif new_y > game.screen_height - self.size[1] // 2:
            new_y = game.screen_height - self.size[1] // 2

        self.set_destination(new_x, new_y)

    def get_buff(self, game, buff):
        if buff == 'shield':
            self.protection_hp += 1
            self.protection.set_alpha(self.protection_hp * 30)
        if buff == 'evil':
            self.shoot_interval //= 2
            self.move_interval_range[0] = int(self.move_interval_range[0] * 0.5)
            self.move_interval_range[1] = int(self.move_interval_range[1] * 0.5)
            if self.shoot_interval < 30: self.shoot_interval = 30
            self.sprite.fill(colors.salmon, special_flags=pg.BLEND_RGBA_MULT)
        if buff == 'lucky':
            for drop in self.drop_chances:
                self.drop_chances[drop] *= 2
            self.sprite.fill(colors.lime, special_flags=pg.BLEND_RGBA_MULT)
        if buff == 'duplicate':
            bandit = game.bandit_pool_dict[self.name].get()
            bandit.spawn(self.rect.center, None, None)
            bandit.push_velocity = (randint(-5, 5), randint(-5, 5))
            bandit.sprite.fill(colors.light_orange, special_flags=pg.BLEND_RGBA_MULT)
            game.level.bandits.append(bandit)

    def get_target(self, game):
        if self.name == 'hitman' and game.player_1:
            possible_targets = [game.player_1, game.player_2 if game.player_2 else game.player_1]
            target = possible_targets[randint(0, 1)]
        elif self.name == 'dicer':
            target = choice(game.level.bandits)
            if target == self:
                target = choice(game.ufo.blocks)
        else:
            target = choice(game.ufo.blocks)

        if target:
            if hasattr(target, 'rect'):
                self.target = target
            else:
                raise ValueError(f'Invalid target: {target}, argument must be '
                                 f'any class containing a "rect" attribute.')

    def despawn(self, game):
        top_distance = [(0, -3), 0 + self.rect.y]
        bottom_distance = [(0, 3), game.screen_height - self.rect.y]
        left_distance = [(-3, 0), 0 + self.rect.x]
        right_distance = [(3, 0), game.screen_width - self.rect.x]
        smallest_x = min(left_distance[1], right_distance[1])
        smallest_y = min(top_distance[1], bottom_distance[1])

        if smallest_x < smallest_y:
            side_goal = left_distance if smallest_x == left_distance[1] else right_distance
        else:
            side_goal = top_distance if smallest_y == top_distance[1] else bottom_distance

        self.despawning = True
        self.set_velocity(side_goal[0])

    def shoot(self, game, target):
        direction_x = target.rect.centerx - self.rect.centerx
        direction_y = target.rect.centery - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if magnitude != 0 and self.can_shoot:
            direction = (int((direction_x / magnitude) * self.bullet_speed),
                         int((direction_y / magnitude) * self.bullet_speed))

            new_bullet = game.bullet_pool_dict[self.bullet_type].get()
            new_bullet.spawn(self.rect.center, direction, self)
            game.level.bullets.append(new_bullet)

            game.sound.play_sfx('bandit_shoot')

    def damage(self, game, damage):
        if self.alive:
            game.sound.play_sfx('bandit_damage')

            if self.protection_hp > 0:
                self.protection_hp = max(0, self.protection_hp - damage)
                self.protection.set_alpha(self.protection_hp * 30)
            else:
                self.health = max(0, self.health - damage)
                if self.health < 1:
                    self.kill()
                    game.level.spawn_pickup(self.get_drop(), self.rect.center)

    def push_check(self, game, player):
        if not player:
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and player.alive and self.can_push:
            self.push(shield_rect)
            game.sound.play_sfx('push')
            game.data[f"p{player.id}_stats"]["bandits_pushed"] += 1

            if self.lifetime < 2:
                self.lifetime = 2

    def update(self, game):
        self.get_target(game)
        self.push_check(game, game.player_1)
        self.push_check(game, game.player_2)

        if self.stuck and self.push_velocity == (0, 0):
            self.set_velocity(0, 0)

        super().update(game)
        self.movement_rect.center = self.rect.center
        self.protection_rect.center = self.rect.center

        if not self.is_moving:
            self.move_tick += 1

        self.shoot_tick += 1

        # Initial movement to appear on screen
        if self.lifetime <= 2 and self.spawn_grace and self.push_velocity == (0, 0):
            self.rect.x += (self.spawnpoint[0] - self.rect.x) * 0.05
            self.rect.y += (self.spawnpoint[1] - self.rect.y) * 0.05
        elif self.spawn_grace:
            self.spawn_grace = False
            self.get_random_destination(game)

        # Randomly moving the bandit
        if self.move_tick >= self.move_interval and not self.spawn_grace:
            self.is_moving = True
            self.move_interval = randint(self.move_interval_range[0], self.move_interval_range[1])
            self.move_tick = 0
            self.get_random_destination(game)

        if self.lifetime > self.despawn_time:
            self.despawn(game)

        # Updating shooting system
        if (self.shoot_tick >= self.shoot_interval and self.target
                and self.can_shoot and not self.stuck):
            self.shoot_tick = 0
            self.shoot(game, self.target)

    def draw(self, game):
        if game.debug:
            game.screen.blit(self.movement_surface, self.movement_rect)

        super().draw(game)

        if self.protection_hp > 0:
            game.screen.blit(self.protection, self.protection_rect)


