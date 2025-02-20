"""
Class for spawning bullet_sprites and handling their behaviour,
they have a position to be spawned at and a direction to constantly go.
"""
from random import randint, choice
import math

from components.game_object import GameObject
from utils.colors import Colors
colors = Colors()

class Bullet(GameObject):
    def __init__(self, bullet_config, bullet_id=None):
        super().__init__(bullet_config, bullet_id)

        self.random_buff = None
        self.wild_tick = [0, randint(15, 60)]
        self.times_reflected = 0
        self.sfx_interval = 0
        self.screen_limited = True
        self.max_velocity = 5
        self.max_lifetime = 10

        if self.type == 'card':
            self.set_buff(choice(['protection', 'wild', 'evil', 'lucky']))

    def reset(self):
        super().reset()
        self.random_buff = None
        self.times_reflected = 0
        self.wild_tick = [0, randint(15, 60)]

    def set_owner(self, owner):
        super().set_owner(owner)

        if self.name == 'bullet':
            self.set_color()

    def set_buff(self, buff):
        self.random_buff = buff
        buff_color = self.color

        if buff == 'protection':
            buff_color = colors.light_blue
        if buff == 'wild':
            buff_color = colors.light_orange
        if buff == 'evil':
            buff_color = colors.crimson
        if buff == 'lucky':
            buff_color = colors.lime
            self.max_lifetime = 4

        self.set_color(buff_color)

    # Constantly update the instance
    def update(self, game):
        super().update(game)
        self.sfx_interval += 1

        if self.random_buff and self.random_buff == 'wild':
            self.wild_tick[0] += 1
            if self.wild_tick[0] >= self.wild_tick[1]:
                self.wild_tick[0] = 0
                self.wild_tick[1] = randint(15, 60)
                new_x = randint(-5, 5)
                new_y = randint(-5, 5)
                while new_x not in (-1, 0, 1) or new_y not in (-1, 0, 1):
                    new_x = randint(-5, 5)
                    new_y = randint(-5, 5)
                self.set_velocity(new_x, new_y)

    def reflect(self, rect, player=None, game=None):
        self.times_reflected += 1

        # Get the relative position of the collision
        relative_collision_x = (self.rect.centerx - rect.left) / rect.width
        relative_collision_y = (self.rect.centery - rect.top) / rect.height
        offset_y = (relative_collision_y - 0.5)
        offset_x = (relative_collision_x - 0.5)

        # Adjust direction depending on bullet movement
        speed_x = int(offset_x * self.max_velocity)
        speed_y = int(offset_y * self.max_velocity)

        if self.sfx_interval >= 15:
            self.sfx_interval = 0
            game.sound.play_sfx('bounce')

        if player and game:
            self.set_owner(player)

            if 'bullet_size' in player.PU_list:
                boost = 0
                if self.times_reflected <= player.PU_list['bullet_size']:
                    boost = 3 * player.PU_list['bullet_size']
                elif self.times_reflected < 16 and self.name == 'bullet':
                    boost = 2
                elif self.times_reflected < 8 and self.name == 'card':
                    boost = 2

                if boost > 0:
                    self.set_size(self.size[0] + boost, self.size[1] + boost)

            if 'extra_reflect' in player.PU_list:
                BASE_SPREAD_ANGLE = 25
                MAX_SPREAD = 90

                # Get base reflection angle
                base_angle = math.atan2(speed_y, speed_x)
                extra_count = player.PU_list['extra_reflect']

                # Determine total spread (increase with bullet count)
                spread_angle = min(BASE_SPREAD_ANGLE * extra_count, MAX_SPREAD)

                # Generate spread angles
                angles = [
                    base_angle + math.radians(spread_angle * (i - (extra_count - 1) / 2) / max(extra_count - 1, 1))
                    for i in range(extra_count)]

                for angle in angles:
                    speed_x = math.cos(angle) * self.max_velocity
                    speed_y = math.sin(angle) * self.max_velocity
                    new_bullet = game.bullet_pool_dict[self.name].get()
                    new_bullet.spawn(self.rect.center, (speed_x, speed_y), player)

        # Adjust direction depending on bullet movement
        speed_x = round(speed_x * self.max_velocity, 1)
        speed_y = round(speed_y * self.max_velocity, 1)
        if speed_x == 0 == speed_y:
            speed_x = self.velocity_x * -1
            speed_y = self.velocity_y * -1

        self.set_velocity(speed_x, speed_y)

    def collide_check(self, game, player):
        if not player or self.owner.type == 'player':
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and self.owner.type == 'enemy' and player.alive:
            # Convert bullet's ownership to the player, now allowing it to damage enemies
            self.reflect(shield_rect, player, game)
            self.set_owner(player)
            game.data[f"p{player.id}_stats"]["bullets_reflected"] += 1
        '''elif self.owner.type == 'enemy' and player.alive:
            if 'magnet' in player.PU_list:
                self.follow_strength = 1 + player.PU_list['magnet'] / 4
                self.max_magnitude = 50 + 20 * player.PU_list['magnet']
                super().follow(shield_rect)'''

        if self.rect.colliderect(player.hitbox) and player.alive and self.owner.type == 'enemy':
            # Deactivate shield and start cooldown timer if hit player
            player.damage(game)
            self.kill()

