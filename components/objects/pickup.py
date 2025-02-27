import pygame as pg
from random import randint

from components.game_object import GameObject
from components.hazzards.explosion import Explosion
from utils.text import Text
from assets import TEXT_FONT, UI_CACHE

from utils.colors import Colors
colors = Colors()

class PickUp(GameObject):
    def __init__(self, config, pickup_id=None):
        super().__init__(config, pickup_id)
        self.alive = True
        self.has_frame = True
        self.frame_visible = True

        self.frame = UI_CACHE['item_frame'].copy()
        self.frame = pg.transform.scale(self.frame, self.size)
        self.pointer = Text('v', (0, 0), TEXT_FONT, colors.light_yellow)
        self.pointer.rect = (self.rect.centerx, self.rect.centery - self.size[1])

        self.stay_within_screen = True
        self.can_collect = True
        self.can_explode = False
        self.can_hold = ['turret_shooter', 'turret_shield']

        self.blink_seconds = 3
        self.explode = [False, 0, 90, False, False]

        self.pointer_tick = 0
        self.pointer_interval = 20
        self.pointer_pos = 5
        self.can_follow = True

        # Configuration depending on item type
        self.max_lifetime = config['despawn_time']
        self.frame.fill(config['frame_color'], special_flags=pg.BLEND_RGBA_MULT)
        if self.type == 'brick':
            self.has_frame = False

        if self.name == 'bomb' or self.name == 'gift_bomb':
            self.can_collect = False
            self.has_frame = False
            self.can_push = True
            self.can_explode = True
            self.can_follow = False

    def collide_check(self, game, player):
        if not player:
            return

        if 'magnet' in player.PU_list and self.can_follow:
            self.follow_strength = player.PU_list['magnet'] + 1
            self.max_magnitude = 100 + 20 * player.PU_list['magnet']
            self.follow(player.rect)

        if self.can_push:
            self.push_check(player)

        # Apply different functions depending on the object, if player collected
        if self.rect.colliderect(player.hitbox):
            if self.type == 'power_up' and self.can_collect:
                game.data[f"p{player.id}_stats"]["powerups_collected"] += 1
                player.get_powerup(game, self.name)
            if self.type == 'item' and self.can_collect:
                if self.name in self.can_hold and player.holding:
                    return

                game.data[f"p{player.id}_stats"]["items_collected"] += 1
                player.get_item(game, self.name)
            if self.type == 'brick' and self.can_collect:
                game.data[f"p{player.id}_stats"]["items_collected"] += 1
                brick_amount = 0

                if self.name == 'brick': brick_amount = 1
                if self.name == 'double_brick': brick_amount = 2
                if self.name == 'brick_pile': brick_amount = 5

                if 'extra_block' in player.PU_list:
                    extra_chance = [0, 50, 120, 250]
                    extra_chance = extra_chance[player.PU_list['extra_block']]

                    for extra in range(0, 1 + extra_chance // 100):
                        if extra_chance - (100 * extra) > randint(1, 100):
                            brick_amount += 1

                game.ufo.heal(game, brick_amount, player)

            self.alive = False

    def push_check(self, player):
        if not player:
            return

        collided = None
        # Check if the player's shield is being hit
        if self.rect.colliderect(player.shield_rect) and player.alive:
            collided = player.shield_rect
        elif self.rect.colliderect(player.hitbox):
            collided = player.rect

        if collided:
            self.push(collided)

    def update(self, game):
        super().update(game)
        if self.lifetime >= self.max_lifetime - self.blink_seconds and not self.can_blink:
            self.set_blink(True)

        self.collide_check(game, game.player_1)
        self.collide_check(game, game.player_2)
        self.bomb_check(game)

        new_y = self.rect.centery - self.size[1] - self.pointer_pos
        self.pointer.rect = (self.rect.centerx, new_y)

        if self.tick % self.pointer_interval == 0:
            self.pointer_pos = -self.pointer_pos

    def bomb_check(self, game):
        if self.can_explode:
            self.explode[1] += 1

            if 3 <= self.lifetime < 5:
                if not self.explode[4]:
                    self.explode[4] = True
                    self.set_blink(True, 30)

                if self.explode[1] % 4 == 0:
                    if self.explode[3]:
                        self.set_color(colors.ruby)
                    else:
                        self.set_color(colors.orange)

                if self.explode[1] >= 8:
                    self.explode[1] = 0
                    self.explode[3] = not self.explode[3]
                    self.blink_interval -= 2 if self.blink_interval > 8 else 1
            elif self.lifetime >= 5 and not self.explode[0]:  # Creating the explosion
                self.alive = False
                self.explode[0] = False
                if self.name != 'gift_bomb':
                    explosion_size = (self.size[0] * 3, self.size[1] * 3)
                else:
                    explosion_size = (self.size[0] * 4, self.size[1] * 4)

                new_explosion = Explosion(game, self.rect.center, explosion_size)
                game.level.objects.append(new_explosion)

                if self.name == 'gift_bomb':
                    new_explosion.set_color(colors.light_red, colors.sea_green)

    def blink_frame(self):
        if self.tick % self.blink_interval == 0:
            self.frame_visible = not self.frame_visible

    def draw(self, game):
        super().draw(game)
        self.blink_frame()

        if self.visible:
            if self.can_collect:
                self.pointer.draw(game)

            if self.frame_visible and self.has_frame:
                game.screen.blit(self.frame, self.rect)