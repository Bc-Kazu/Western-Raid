"""
Class for spawning bullet_sprites and handling their behaviour,
they have a position to be spawned at and a direction to constantly go.
"""
from random import randint, choice
import math
import pygame as pg

from components.game_object import GameObject
from components.hazzards.explosion import Explosion
from utils.colors import Colors
colors = Colors()

class Bullet(GameObject):
    def __init__(self, bullet_config, bullet_id=None):
        super().__init__(bullet_config, bullet_id)

        self.buff = None
        self.wild_tick = [0, randint(15, 60)]
        self.times_reflected = 0
        self.screen_reflected = 0
        self.sfx_interval = 0
        self.screen_limited = True
        self.max_velocity = 10
        self.max_lifetime = 10
        self.explosion_size = (3 * self.size[0], 3 * self.size[1])
        self.can_explode = False
        self.is_extra = False

        self.screen_reflect_tick = 0
        self.screen_reflect_interval = 15

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        super().spawn(position, velocity, owner)

        if self.name == 'card':
            self.reset_sprite()
            self.set_buff(choice(['protection', 'duplicate', 'evil', 'lucky']))
        if self.name == 'dynamite':
            self.reset_sprite()
            self.set_color()
            self.can_explode = True
            self.explosion_size = (3 * self.size[0], 3 * self.size[1])

    def reset(self):
        super().reset()
        self.buff = None
        self.times_reflected = 0
        self.screen_reflected = 0
        self.wild_tick = [0, randint(15, 60)]

    def set_owner(self, owner):
        super().set_owner(owner)

        if self.name == 'bullet' or self.name == 'dynamite':
            self.set_color()

    def set_buff(self, buff):
        self.buff = buff
        buff_color = self.color

        if buff == 'protection':
            buff_color = colors.light_blue
        if buff == 'duplicate':
            buff_color = colors.light_orange
        if buff == 'evil':
            buff_color = colors.crimson
        if buff == 'lucky':
            buff_color = colors.lime

        self.set_color(buff_color)

    # Constantly update the instance
    def update(self, game):
        self.collide_check(game)
        super().update(game)
        self.sfx_interval += 1

        speed = int((self.velocity_x**2 + self.velocity_y**2) ** 0.7)
        rotate_interval = max(20 - speed, 5)
        if self.name == 'dynamite' and self.tick % rotate_interval == 0:
            self.sprite = pg.transform.rotate(self.sprite, 90)

        self.screen_reflect_tick += 1
        can_reflect = 0 < self.times_reflected and self.screen_reflected < 1
        if can_reflect and self.owner and self.owner.type == 'player':
            if self.screen_reflect_tick > self.screen_reflect_interval:
                if self.rect.left <= 0 or self.rect.right >= game.screen_width:
                    if self.velocity_y == 0:
                        self.velocity_y = randint(-5, 5)
                    self.velocity_x *= -1
                    self.screen_reflect_tick = 0
                    self.screen_reflected += 1
                if self.rect.top <= 0 or self.rect.bottom >= game.screen_height:
                    if self.velocity_x == 0:
                        self.velocity_x = randint(-5, 5)
                    self.velocity_y *= -1
                    self.screen_reflect_tick = 0
                    self.screen_reflected += 1

    def reflect(self, rect, player=None, game=None):
        self.times_reflected += 1
        self.set_max_velocity(5)

        # Get the relative position of the collision
        relative_collision_x = (self.rect.centerx - rect.left) / rect.width
        relative_collision_y = (self.rect.centery - rect.top) / rect.height
        offset_y = (relative_collision_y - 0.5)
        offset_x = (relative_collision_x - 0.5)

        # Adjust direction depending on bullet movement
        speed_x = int(offset_x * self.max_velocity)
        speed_y = int(offset_y * self.max_velocity)
        speed_x = min(max(round(speed_x * 5, 1), -5), 5)
        speed_y = min(max(round(speed_y * 5, 1), -5), 5)

        # Adjust direction depending on bullet movement
        if speed_x == 0 == speed_y:
            speed_x = self.velocity_x * -1
            speed_y = self.velocity_y * -1

        self.set_velocity(speed_x, speed_y)

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

            extra_count = player.PU_list.get('extra_reflect', 0)
            success = randint(0, 50 + 10 * extra_count) > randint(0, 100)
            if extra_count > 0 and success:
                angle = 15 * extra_count
                self.spread(game, extra_count, angle)

        if self.sfx_interval >= 15:
            self.sfx_interval = 0
            game.sound.play_sfx('bounce')

    def spread(self, game, count, spread_angle=45, max_angle=90):
        # Get base reflection angle
        base_angle = math.atan2(self.velocity_y, self.velocity_x)
        total_bullets = count + 1

        # Determine total spread (increase with bullet count)
        spread_angle = min(spread_angle * count, max_angle)

        # Generate spread angles
        angles = [
            base_angle + math.radians(spread_angle * (i - (total_bullets - 1) / 2) / max(total_bullets - 1, 1))
            for i in range(total_bullets)]

        for bullet_angle in angles:
            speed_x = math.cos(bullet_angle) * 5
            speed_y = math.sin(bullet_angle) * 5
            self.spawn_from_self(game, (speed_x, speed_y))

        self.kill()
        self.can_explode = False

    def spawn_from_self(self, game, velocity, can_reflect=True):
        new_bullet = game.bullet_pool_dict[self.name].get()
        new_bullet.set_max_velocity(5)
        new_bullet.spawn(self.rect.center, velocity, self.owner)
        new_bullet.set_size(self.size)
        game.level.bullets.append(new_bullet)

        if can_reflect:
            new_bullet.times_reflected += 1

    def player_collide(self, game, player):
        if not player or not self.owner or not player.alive:
            return

        # Check player shield collision to apply bullet reflection
        if self.rect.colliderect(player.shield_rect) and self.owner.type == 'enemy':
            self.reflect(player.shield_rect, player, game)
            self.set_owner(player)
            game.data[f"p{player.id}_stats"]["bullets_reflected"] += 1
        # Check if the player is being hit to damage them
        elif self.rect.colliderect(player.hitbox) and self.owner.type == 'enemy':
            player.damage(game)
            self.kill()

    def explode(self, game):
        self.kill()
        new_explosion = Explosion(game, self.rect.center, self.explosion_size, 'explode2')
        new_explosion.set_lifetick(20)
        game.level.objects.append(new_explosion)

    def collide_check(self, game):
        if not self.alive:
            return

        self.player_collide(game, game.player_1)
        self.player_collide(game, game.player_2)

        for bandit in game.level.bandits:
            if not self.alive:
                break
            if not bandit.alive or not bandit.can_collide:
                continue

            # Verify bullet collision with bandit
            if self.rect.colliderect(bandit.rect):
                # Verify if bullet has a buff effect
                if self.buff and self.spawner != bandit:
                    bandit.get_buff(game, self.buff)
                    game.sound.play_sfx('buff')
                    self.kill()
                # Damaging the bandit
                elif self.owner and self.owner.type == 'player':
                    bandit.damage(game, 1)
                    self.kill()

                    if not bandit.alive:
                        self.owner.get_score(game, bandit.points_value, True, bandit.rect.center)

                    if not self.alive:
                        game.data[f"p{self.owner.id}_stats"]["bandits_killed"] += 1
                        break

        if not self.alive and self.can_explode:
            self.explode(game)

