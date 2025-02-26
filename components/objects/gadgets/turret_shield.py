import math

from components.game_object import GameObject
from assets import GADGET_CACHE, TEXT_FONT

import pygame as pg
from utils.colors import Colors
from utils.text import Text
colors = Colors()

class TurretShield(GameObject):
    def __init__(self, config, turret_id=None):
        super().__init__(config, turret_id)
        self.base_health = 5
        self.health = self.base_health

        # Other sprites settings
        self.base_sprite = self.sprite.copy()
        self.orb_sprite = GADGET_CACHE['orb'].copy()
        self.orb_sprite = pg.transform.scale(self.orb_sprite, (25, 25))
        self.orb_rect = self.orb_sprite.get_rect()

        # Object state settings
        self.can_place = True
        self.is_placed = False
        self.placing_time = 4

        self.pointer = Text('v', (0, 0), TEXT_FONT, colors.light_yellow)
        self.pointer.rect = (self.rect.centerx, self.rect.centery - self.size[1])
        self.pointer_tick = 0
        self.pointer_interval = 20
        self.pointer_pos = 5
        
        # Shield settings
        self.shield = pg.Surface((150,  150), pg.SRCALPHA)
        self.shield.fill(colors.white)
        self.shield.set_alpha(15)
        self.shield_rect = self.shield.get_rect()
        self.shield_rect.center = self.rect.center

        self.shield_base_max = 5
        self.shield_max_health = self.shield_base_max
        self.shield_health = self.shield_max_health
        self.shield_interval = 300

        self.place_timer = Text(str(self.placing_time), (0, 0), TEXT_FONT, colors.window_white)
        self.place_timer.rect = (self.rect.centerx, self.rect.centery)

        self.health_indicator = Text(str(self.health), (0, 0), TEXT_FONT, colors.pure_shadow)
        self.health_indicator.rect = (self.rect.centerx, self.rect.centery)

    def kill(self):
        super().kill()
        if self.owner.holding == self:
            self.owner.holding = None

    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.health = self.base_health
        self.health += 1 * owner.PU_list.get('recovery', 0)
        self.shield_max_health = self.shield_base_max
        self.shield_max_health += 3 * owner.PU_list.get('space_shield', 0)
        
        super().spawn(position, velocity, owner)

        size_x, size_y = 150, 150
        size_x += 25 * owner.PU_list.get('extra_block', 0)
        size_x += 25 * owner.PU_list.get('shield_size', 0)
        size_y += 25 * owner.PU_list.get('extra_block', 0)
        size_y += 25 * owner.PU_list.get('shield_size', 0)

        self.shield_health = self.shield_max_health
        self.shield_interval = 300 - 30 * owner.PU_list.get('recovery', 0)

        self.shield = pg.Surface((size_x, size_y), pg.SRCALPHA)
        self.shield.fill(colors.white)
        self.shield.set_alpha(15)
        self.shield_rect = self.shield.get_rect()
        self.shield_rect.center = self.rect.center

        # Recoloring the orb image to the player's color
        self.orb_sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        self.can_place = True
        self.is_placed = False
        # Transparent sprites to indicate placement mode
        self.sprite.set_alpha(128)
        self.orb_sprite.set_alpha(128)

    def place(self, game):
        self.is_placed = True
        self.sprite.set_alpha(255)
        self.orb_sprite.set_alpha(255)
        self.owner.holding = None
        game.sound.play_sfx('brick_get')

        self.shield.fill(self.owner.color)
        self.shield_update(0)

    def shield_update(self, health):
        self.shield_health += health
        if self.shield_health > self.shield_max_health:
            self.shield_health = self.shield_max_health
        elif self.shield_health < 0:
            self.shield_health = 0

        alpha = min(255, int(20 * math.log(self.shield_health + 1)))
        self.shield.set_alpha(alpha)

    def update(self, game):
        super().update(game)

        self.shield_rect.center = self.rect.center
        self.orb_rect.center = self.rect.center
        self.orb_rect.y -= self.orb_sprite.get_size()[1] // 2

        if self.is_placed:
            self.collide_check(game)

            if self.tick % self.shield_interval == 0:
                self.shield_update(1)
        else:
            self.rect.center = self.owner.rect.center
            self.rect.x += 50 * self.owner.last_direction[0]
            self.rect.y += 50 * self.owner.last_direction[1]

            time_left = str(self.placing_time - self.lifetime)
            self.place_timer.set_text(time_left)
            self.place_timer.set_position(self.owner.rect.centerx, self.owner.rect.y - 40)

            new_y = self.rect.centery - self.size[1] - self.pointer_pos
            self.pointer.rect = (self.rect.centerx, new_y)

            if self.tick % self.pointer_interval == 0:
                self.pointer_pos = -self.pointer_pos

            if self.lifetime > self.placing_time and self.can_place:
                self.place(game)

            # Detect if place area is not allowed
            if self.rect.colliderect(game.ufo.rect):
                self.can_place = False
                self.place_timer.set_text('[ X ]')
                self.place_timer.set_color(colors.light_red)

                if game.tick % game.FPS == 0:
                    self.lifetime -= 1
            else:
                self.can_place = True
                self.place_timer.set_color(colors.white)

        self.health_indicator.set_text(str(self.health))
        self.health_indicator.set_position(self.rect.center)

    def damage(self, game, damage):
        if self.alive:
            game.sound.play_sfx('block_break')
            self.health = max(0, self.health - damage)
            if self.health < 1:
                game.sound.play_sfx('remove')
                self.kill()

    def collide_check(self, game):
        for bullet in game.level.bullets:
            if not bullet.owner.type == 'enemy':
                continue

            if not self.stuck:
                if self.shield_rect.colliderect(bullet.rect) and self.shield_health > 0:
                    self.shield_update(-1)

                    game.sound.play_sfx('shield_hit')
                    bullet.reflect(self.shield_rect, self.owner, game)
                    return

            # Verify bullet collision with bandit
            if bullet.rect.colliderect(self.rect) and bullet.alive:
                if bullet.owner.type == 'enemy':
                    self.damage(game, 1)
                    bullet.kill()

                    if bullet.name == 'dynamite':
                        bullet.explode(game)


    def draw(self, game):
        super().draw(game)

        if self.visible:
            game.screen.blit(self.sprite, self.rect)
            game.screen.blit(self.orb_sprite, self.orb_rect)
            game.screen.blit(self.shield, self.shield_rect)

            if not self.is_placed:
                self.pointer.draw(game)
                self.place_timer.draw(game)

        if game.debug:
            self.health_indicator.draw(game)





