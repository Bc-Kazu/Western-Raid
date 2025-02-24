import math
from random import randint, choice

from components.game_object import GameObject
from assets import GADGET_CACHE, TEXT_FONT

import pygame as pg
from utils.colors import Colors
from utils.text import Text

colors = Colors()

def load_sprite(bot, name):
    image = GADGET_CACHE[name].copy()
    image = pg.transform.scale(image, bot.size)
    bot.sprite_dict[name] = image
    return image

class BotShooter(GameObject):
    def __init__(self, config, turret_id=None):
        super().__init__(config, turret_id)
        self.base_health = 15
        self.health = self.base_health
        self.sprite_dict = {}

        # Other sprites settings
        self.base_sprite = self.sprite.copy()
        self.base_eyes_sprite = load_sprite(self, 'bot_base_eyes')
        self.closed_eyes_sprite = load_sprite(self, 'bot_closed_eyes')
        self.sad_eyes_sprite = load_sprite(self, 'bot_sad_eyes')
        self.happy_eyes_sprite = load_sprite(self, 'bot_happy_eyes')
        self.current_eyes = self.base_eyes_sprite

        # Object state settings
        self.is_placed = False
        self.stay_within_screen = True

        self.health_indicator = Text(str(self.health), (0, 0), TEXT_FONT, colors.pure_shadow)
        self.health_indicator.rect = (self.rect.centerx, self.rect.centery)

        # Shooting settings
        self.can_shoot = True
        self.bullet_type = 'bullet'
        self.bullet_speed = 4
        self.shoot_tick = 0
        self.base_shoot_interval = 200
        self.shoot_interval = self.base_shoot_interval

        self.shoot_range = 300
        self.shoot_rect = pg.Rect(self.rect.center, (self.shoot_range, self.shoot_range))
        self.shoot_area = pg.Surface((self.shoot_range, self.shoot_range), pg.SRCALPHA)
        self.shoot_area.fill(colors.white)
        self.shoot_area.set_alpha(15)

        self.victory_offset = choice([-15, 15])

        # Movement settings
        self.move_range = 400
        self.move_interval = 0
        self.move_interval_base = [30, 120]
        self.move_interval_range = self.move_interval_base[:]
        self.move_tick = self.move_interval

        self.find_interval_base = 360
        self.find_interval = self.find_interval_base
        self.find_tick = 0

        self.movement_surface = pg.Surface((self.move_range, self.move_range), pg.SRCALPHA)
        self.movement_surface.fill(colors.cyan)
        self.movement_surface.set_alpha(10)
        self.movement_rect = pg.Rect(0, 0, self.move_range, self.move_range)


    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.health = self.base_health
        self.health += 2 * owner.PU_list.get('recovery', 0)
        self.health += 4 * owner.PU_list.get('space_shield', 0)
        self.shoot_tick = 0
        self.shoot_interval = self.base_shoot_interval - 30 * owner.PU_list.get('auto_shoot', 0)
        super().spawn(position, velocity, owner)
        self.set_color(owner.color)

        self.shoot_range = 300 + 80 * owner.PU_list.get('magnet', 0)
        self.shoot_rect = pg.Rect(self.rect.center, (self.shoot_range, self.shoot_range))
        self.shoot_area = pg.Surface((self.shoot_range, self.shoot_range), pg.SRCALPHA)
        self.shoot_area.fill(colors.white)
        self.shoot_area.set_alpha(15)

        self.find_interval = self.find_interval_base - 60 * owner.PU_list.get('magnet', 0)
        self.destined_velocity = 2 + 1 * owner.PU_list.get('ghost_fury', 0)
        self.is_placed = False

    def place(self, game):
        self.is_placed = True
        game.sound.play_sfx('brick_get')

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

    def get_enemy_destination(self, game):
        if len(game.level.bandits) > 0:
            random_target = choice(game.level.bandits)
            new_x = random_target.rect.centerx
            new_y = random_target.rect.centery

            if new_x < self.rect.centerx:
                new_x += 100
            elif new_x > self.rect.centerx:
                new_x -= 100
            if new_y < self.rect.centery:
                new_y += 100
            elif new_y > self.rect.centery:
                new_y -= 100

            self.set_destination(new_x, new_y)


    def update(self, game):
        super().update(game)
        self.shoot_rect.center = self.rect.center
        self.movement_rect.center = self.rect.center

        if self.is_placed:
            if game.level.defeat:
                self.set_velocity(0, 0)
                return
            elif game.victory_transition[2]:
                self.set_velocity(0, 0)

                if game.tick % 15 == 0:
                    self.rect.y = self.rect.y + self.victory_offset
                    self.victory_offset = -self.victory_offset
                return


            self.shoot_tick += 1
            self.move_tick += 1
            self.find_tick += 1
            self.collide_check(game)

            # Updating shooting system
            lower_interval = 0
            if not self.owner.alive:
                lower_interval = 15 * self.owner.PU_list.get('ghost_fury', 0)

            if not self.stuck:
                if self.shoot_tick >= self.shoot_interval - lower_interval and self.can_shoot:
                    self.shoot_tick = 0
                    self.shoot(game)

                # Randomly moving the bandit
                if self.move_tick >= self.move_interval and not self.is_moving:
                    self.move_interval = randint(self.move_interval_range[0], self.move_interval_range[1])
                    self.move_tick = 0
                    self.get_random_destination(game)

                if self.find_tick >= self.find_interval:
                    self.find_tick = 0
                    self.get_enemy_destination(game)
            else:
                self.set_velocity(0, 0)
        else:
            self.place(game)

        self.health_indicator.set_text(str(self.health), self.rect.center)

    def shoot(self, game):
        bullets_shot = 0

        for bandit in game.level.bandits:
            if self.shoot_rect.colliderect(bandit.rect):
                bandit_x = bandit.rect.centerx
                bandit_y = bandit.rect.centery
                direction_x = bandit_x - self.rect.centerx
                direction_y = bandit_y - self.rect.centery
                magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

                if self.shoot_range > magnitude > 0:
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

        if game.debug:
            game.screen.blit(self.shoot_area, self.shoot_rect)

        if self.visible:
            game.screen.blit(self.sprite, self.rect)

            if game.victory_transition[2]:
                self.current_eyes = self.happy_eyes_sprite
            elif game.level.defeat or self.stuck:
                self.current_eyes = self.sad_eyes_sprite
            else:
                if self.health <= 3:
                    self.current_eyes = self.closed_eyes_sprite
                else:
                    self.current_eyes = self.base_eyes_sprite

            offset_rect = self.rect.copy()
            offset_rect.x += max(min(self.velocity_x * 2, 5), -5)
            offset_rect.y += max(min(self.velocity_y * 2, 5), -5)

            if game.level.defeat:
                offset_rect.center = self.rect.center
                offset_rect.y += 2

            game.screen.blit(self.current_eyes, offset_rect)

        if game.debug:
            self.health_indicator.draw(game)





