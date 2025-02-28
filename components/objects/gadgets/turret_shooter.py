import math

from components.game_object import GameObject
from assets import GADGET_CACHE, TEXT_FONT

import pygame as pg
from utils.colors import Colors
from utils.text import Text

colors = Colors()

def load_sprite(turret, name):
    image = GADGET_CACHE['turret_shooter_' + name].copy()
    image = pg.transform.scale(image, turret.size)
    turret.aim_sprite_dict[name] = image
    return image

class TurretShooter(GameObject):
    def __init__(self, config, turret_id=None):
        super().__init__(config, turret_id)
        self.base_health = 10
        self.health = self.base_health
        self.aim_sprite_dict = {}
        self.offscreen_limit = 0

        # Other sprites settings
        self.base_sprite = self.sprite.copy()
        self.up_sprite = load_sprite(self, 'up')
        self.down_sprite = load_sprite(self, 'down')
        self.left_sprite = load_sprite(self, 'left')
        self.right_sprite = load_sprite(self, 'right')
        self.current_direction = 'right'

        # Object state settings
        self.is_placed = False
        self.placing_time = 4

        self.pointer = Text('v', (0, 0), TEXT_FONT, colors.light_yellow)
        self.pointer.rect = (self.rect.centerx, self.rect.centery - self.size[1])
        self.pointer_tick = 0
        self.pointer_interval = 20
        self.pointer_pos = 5

        self.place_timer = Text(str(self.placing_time), (0, 0), TEXT_FONT, colors.window_white)
        self.place_timer.rect = (self.rect.centerx, self.rect.centery)

        self.health_indicator = Text(str(self.health), (0, 0), TEXT_FONT, colors.pure_shadow)
        self.health_indicator.rect = (self.rect.centerx, self.rect.centery)

        # Shooting settings
        self.can_shoot = True
        self.bullet_type = 'bullet'
        self.bullet_speed = 4
        self.shoot_tick = 0
        self.base_shoot_interval = 120
        self.shoot_interval = self.base_shoot_interval

        self.shoot_range = 300
        self.shoot_rect = pg.Rect(self.rect.center, (self.shoot_range, self.shoot_range))
        self.shoot_area = pg.Surface((self.shoot_range, self.shoot_range), pg.SRCALPHA)
        self.shoot_area.fill(colors.white)
        self.shoot_area.set_alpha(15)

    def kill(self):
        super().kill()
        if self.owner.type == 'player' and self.owner.holding == self:
            self.owner.holding = None

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.health = self.base_health
        self.health += 2 * owner.PU_list.get('recovery', 0)
        self.health += 4 * owner.PU_list.get('space_shield', 0)
        self.shoot_tick = 0
        self.shoot_interval = self.base_shoot_interval - 10 * owner.PU_list.get('auto_shoot', 0)
        super().spawn(position, velocity, owner)

        # Recoloring all the aiming sprites
        self.sprite = self.up_sprite
        super().set_color()
        self.sprite = self.down_sprite
        super().set_color()
        self.sprite = self.left_sprite
        super().set_color()
        self.sprite = self.right_sprite
        super().set_color()
        # Setting sprite back to base image
        self.sprite = self.base_sprite.copy()

        self.shoot_range = 300 + 80 * owner.PU_list.get('magnet', 0)
        self.shoot_rect = pg.Rect(self.rect.center, (self.shoot_range, self.shoot_range))
        self.shoot_area = pg.Surface((self.shoot_range, self.shoot_range), pg.SRCALPHA)
        self.shoot_area.fill(colors.white)
        self.shoot_area.set_alpha(15)

        self.is_placed = False
        # Transparent sprites to indicate placement mode
        self.sprite.set_alpha(128)
        for sprite in self.aim_sprite_dict.values():
            sprite.set_alpha(128)

    def place(self, game):
        self.is_placed = True
        self.sprite.set_alpha(255)
        for sprite in self.aim_sprite_dict.values():
            sprite.set_alpha(255)

        self.owner.holding = None
        game.sound.play_sfx('brick_get')

    def update(self, game):
        super().update(game)
        self.shoot_rect.center = self.rect.center

        if self.is_placed:
            self.shoot_tick += 1
            self.collide_check(game)
            self.screen_limited = True

            if self.stolen:
                return

            # Updating shooting system
            lower_interval = 0
            if not self.owner.alive:
                lower_interval = 15 * self.owner.PU_list.get('ghost_fury', 0)

            if not self.stuck:
                if self.shoot_tick >= self.shoot_interval - lower_interval and self.can_shoot:
                    self.shoot_tick = 0
                    self.shoot(game)
        else:
            self.screen_limited = False
            if self.stolen:
                return

            self.rect.center = self.owner.rect.center
            self.rect.x += 50 * self.owner.last_direction[0]
            self.rect.y += 50 * self.owner.last_direction[1]

            self.rect.clamp_ip(game.screen_limit)

            time_left = str(self.placing_time - self.lifetime)
            self.place_timer.set_text(time_left)
            self.place_timer.set_position(self.owner.rect.centerx, self.owner.rect.y - 40)

            new_y = self.rect.centery - self.size[1] - self.pointer_pos
            self.pointer.rect = (self.rect.centerx, new_y)

            if self.tick % self.pointer_interval == 0:
                self.pointer_pos = -self.pointer_pos

            if self.lifetime > self.placing_time:
                self.place(game)

        self.health_indicator.set_text(str(self.health))
        self.health_indicator.set_position(self.rect.center)

    def shoot(self, game):
        bullets_shot = 0

        for bandit in game.level.bandits:
            if self.shoot_rect.colliderect(bandit.rect):
                if bandit.name == 'robber':
                    continue

                bandit_x = bandit.rect.centerx
                bandit_y = bandit.rect.centery
                direction_x = bandit_x - self.rect.centerx
                direction_y = bandit_y - self.rect.centery
                magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

                if self.shoot_range > magnitude > 0:
                    if abs(bandit_x) > abs(bandit_y) and bandit_x < self.rect.centerx:
                        self.current_direction = 'left'
                    elif abs(bandit_x) > abs(bandit_y) and bandit_x >= self.rect.centerx:
                        self.current_direction = 'right'
                    elif abs(bandit_y) > abs(bandit_x) and bandit_y < self.rect.centery:
                        self.current_direction = 'up'
                    elif abs(bandit_y) > abs(bandit_x) and bandit_y >= self.rect.centery:
                        self.current_direction = 'down'

                    direction = (int((direction_x / magnitude) * self.bullet_speed),
                                 int((direction_y / magnitude) * self.bullet_speed))

                    extra_size = 2 * self.owner.PU_list.get('bullet_size', 0)
                    bullet = game.bullet_pool_dict[self.bullet_type].get()
                    bullet.spawn(self.rect.center, direction, self.owner)
                    size = (bullet.size[0] + extra_size, bullet.size[1] + extra_size)
                    bullet.set_size(size)
                    game.level.bullets.append(bullet)

                    game.sound.play_sfx('turret_shoot')
                    bullets_shot += 1

                    if 'extra_reflect' in self.owner.PU_list:
                        if bullets_shot > self.owner.PU_list['extra_reflect']:
                            break
                    else:
                        break

    def damage(self, game, damage):
        if self.alive:
            game.sound.play_sfx('block_break')
            self.health = max(0, self.health - damage)
            if self.health < 1:
                game.sound.play_sfx('remove')
                self.kill()

    def collide_check(self, game):
        for bullet in game.level.bullets:
            # Verify bullet collision with bandit
            if bullet.rect.colliderect(self.rect) and bullet.alive:
                if bullet.owner.type == 'enemy':
                    self.damage(game, 1)
                    bullet.kill()

                    if bullet.name == 'dynamite':
                        bullet.explode(game)

    def draw(self, game):
        super().draw(game)

        if game.debug or not self.is_placed:
            game.screen.blit(self.shoot_area, self.shoot_rect)

        if self.visible:
            game.screen.blit(self.aim_sprite_dict[self.current_direction], self.rect)

            if not self.is_placed:
                self.pointer.draw(game)
                self.place_timer.draw(game)

        if game.debug:
            self.health_indicator.draw(game)





