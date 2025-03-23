"""
Class responsible for creating the UFO object
"""
from constants import UFO_COLORS
from assets import NORMAL_FONT, UFO_CONFIG
from utils.text import Text
from math import log
from components.game_object import GameObject
from components.objects.block import Block

import pygame as pg

from utils.colors import Colors
colors = Colors()

def check_best_powerup(game, name):
    best = 0
    if game.player_1 and name in game.player_1.PU_list:
        best = game.player_1.PU_list[name]
    if game.player_2 and name in game.player_2.PU_list:
        if not best or best < game.player_2.PU_list[name]:
            best = game.player_2.PU_list[name]

    return best


class UfoBlock(Block):
    def __init__(self, config, index, row, column):
        super().__init__(config)
        self.index = index
        self.row = row
        self.column = column
        self.can_die = False

class Ufo(GameObject):
    def __init__(self):
        super().__init__(UFO_CONFIG)
        self.alive = True

        # Define the UFO grid as a list of lists
        self.block_size = (self.size[0] // 6.7, self.size[1] // 6.7)
        self.blocks = []
        self.shape = [
                  [1, 1, 1],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1]
        ]

        self.pointer = Text('v v v', self.rect.center, NORMAL_FONT, colors.light_yellow)
        self.pointer_cd = 20
        self.pointer_down = False
        self.pointer_pos = 10

        self.color = colors.light_blue
        self.block_colors = UFO_COLORS

        self.space_shield = pg.Surface((int(self.size[0] * 1.5), int(self.size[1] * 1.5)), pg.SRCALPHA)
        self.space_shield.fill(self.color)
        self.space_shield.set_alpha(0)
        self.space_shield_rect = self.space_shield.get_rect()
        self.space_shield_rect.center = self.rect.center

        self.space_shield_max = 0
        self.space_shield_hp = 0
        self.base_shield_cd = 420
        self.space_shield_cd = self.base_shield_cd

        self.regenerate = False
        self.regen_safe = 0
        self.regen_cd = 90
        self.regenerated_blocks = 0
        self.max_blocks_regen = 15
        self.layers_filled = [False, False, False]

        self.got_inside = False
        self.can_get_in = False
        self.visible = False

    def kill(self):
        super().kill()
        if len(self.blocks) > 0:
            for block in self.blocks:
                block.set_strength(0)

    def spawn_blocks(self, game, shape=None, block_colors=None, block_size=None):
        self.blocks = []
        self.shape = shape if shape else self.shape
        self.block_colors = block_colors if block_colors else self.block_colors
        self.block_size = block_size if block_size else self.block_size
        index = 0

        for row_index, strengths in enumerate(self.shape):
            row_width = len(strengths) * self.block_size[0]

            # Calculate the starting x position for the current row
            x = (self.rect.centerx * 2 - row_width) // 2 + 1

            # Add blocks for the current row
            for col_index, strength in enumerate(strengths):
                col_width = len(self.shape) * self.block_size[1]
                y = (self.rect.centery * 2 - col_width) // 2 + 25

                index += 1
                pos = (x + col_index * self.block_size[0], y + row_index * self.block_size[1])
                size = (self.block_size[0] - 3, self.block_size[1] - 3)

                if strength >= 0:
                    new_block = UfoBlock(game.ufo_block_config, index, row_index, col_index)
                    new_block.set_size(size, True)
                    new_block.spawn(pos, None, self)
                    new_block.set_strength(strength)
                    self.blocks.append(new_block)

    def position_blocks(self):
        if len(self.blocks) <= 0:
            return

        index = 0
        for row_index, strengths in enumerate(self.shape):
            row_width = len(strengths) * self.block_size[0]

            # Calculate the starting x position for the current row
            x = (self.rect.centerx * 2 - row_width) // 2 + 1

            # Add blocks for the current row
            for col_index, strength in enumerate(strengths):
                col_width = len(self.shape) * self.block_size[1]
                y = (self.rect.centery * 2 - col_width) // 2 + 25

                pos = (x + col_index * self.block_size[0], y + row_index * self.block_size[1])
                self.blocks[index].set_position(pos)
                index += 1

    def collide_check(self, game):
        if not self.can_collide:
            return

        for bandit in game.level.bandits:
            if (bandit.name == 'bomber' and self.space_shield_rect.colliderect(bandit.rect)
                    and self.space_shield_hp > 0):
                bandit.push(self.space_shield_rect)

        for bullet in game.level.bullets:
            owned_by_player= bullet.owner and bullet.owner.type == 'player'
            if not bullet.alive or owned_by_player:
                continue

            if self.space_shield_rect.colliderect(bullet.rect) and self.space_shield_hp > 0:
                self.space_shield_update(-1)

                game.sound.play_sfx('shield_hit')

                best_extra = game.player_1
                if game.player_2 and 'extra_reflect' in game.player_2.PU_list:
                    if 'extra_reflect' in game.player_1.PU_list:
                        if game.player_2.PU_list['extra_reflect'] > best_extra.PU_list['extra_reflect']:
                            best_extra = game.player_2

                bullet.reflect(game, self.space_shield_rect, best_extra)
                return

            # check the collides by the lists
            if self.blocks:
                blocks_alive = 0

                for block in self.blocks:
                    if block.collide_check(bullet):
                        self.take_damage(game, block)

                        if bullet.name == 'dynamite':
                            bullet.explode(game)
                    if block.strength > 0:
                        blocks_alive += 1

                if blocks_alive <= 0:
                    self.kill()

    def take_damage(self, game, block):
        if block.strength > 1:
            game.sound.play_sfx('block_break_extra')

        game.sound.play_sfx('block_break')

        block.set_strength(block.strength - 1)
        game.data["blocks_destroyed"] += 1

        if self.regenerate and self.regen_safe >= 60:
            self.set_regenerate(False)

    def heal(self, game, amount, player=None):
        # Check for any ufo blocks to heal, if not then give points to player
        healed_blocks = 0

        # Sort blocks by strength (weaker blocks come first)
        sorted_blocks = sorted(self.blocks, key=lambda list_block: list_block.strength)
        overheal = False

        for block in sorted_blocks:
            if healed_blocks >= amount:
                break

            if 0 <= block.strength < 3:
                block.set_strength(block.strength + 1)
                if block.strength >= 2:
                    overheal = True

                healed_blocks += 1
                game.data["blocks_restored"] += 1

        if overheal:
            game.sound.play_sfx('points_extra')

        # Check if all blocks in each layer are fully healed
        for layer in range(1, 3):
            self.layers_filled[layer - 1] = all(block.strength >= layer for block in self.blocks)

        # If no blocks were healed, give points instead
        if healed_blocks < 1:
            if player:
                player.get_score(game, 30 * amount, True, player.rect.midtop)
            else:
                if game.player_2:
                    game.player_1.get_score(game, 10 * amount)
                    game.player_2.get_score(game, 10 * amount)
                else:
                    game.player_1.get_score(game, 15 * amount)

            game.sound.play_sfx('points')
        else:
            game.sound.play_sfx('brick_get')

            if player:
                text = f'+{amount} Block'
                text += 's' if amount > 1 else ''
                game.level.spawn_message('popup', text, player.rect.center)

    def victory_check(self, game):
        check_1 = False
        check_2 = False
        if game.player_1:
            game.player_1.victory_tick += 1
            if game.player_1.victory_tick > game.player_1.victory_cooldown:
                check_1 = self.rect.colliderect(game.player_1.hitbox)
        else: check_1 = True

        if game.player_2:
            game.player_2.victory_tick += 1
            if game.player_2.victory_tick > game.player_2.victory_cooldown:
                check_2 = self.rect.colliderect(game.player_2.hitbox)
        else: check_2 = True

        if not self.got_inside:
            if check_1 and check_2:
                self.got_inside = True
                self.can_get_in = False
                self.always_on_top = True
                return True
            else:
                self.visible = True
                self.can_get_in = True
                return False
        else:
            self.rect.y -= 2

    def space_shield_set(self, game, heal=False):
        one_player = not 'space_shield' in game.player_1.PU_list and not game.player_2
        two_players = (not 'space_shield' in game.player_1.PU_list and
                       (game.player_2 and not 'space_shield' in game.player_2.PU_list))

        if one_player or two_players:
            return

        best_max_health = check_best_powerup(game, 'extra_block')
        best_cooldown = check_best_powerup(game, 'recovery')
        best_size = check_best_powerup(game, 'shield_size')

        max_health = 1 + best_max_health
        cooldown = self.base_shield_cd - (40 * best_cooldown)
        size_x = int(self.size[0] * 1.5) + (20 * best_size)
        size_y = int(self.size[1] * 1.5) + (20 * best_size)

        self.space_shield = pg.Surface((size_x, size_y), pg.SRCALPHA)
        self.space_shield.fill(self.color)
        self.space_shield_rect = self.space_shield.get_rect()
        self.space_shield_rect.center = self.rect.center

        self.space_shield_max = max_health
        self.space_shield_cd = cooldown

        if heal:
            self.space_shield_hp = max_health

        alpha = min(255, int(60 * log(self.space_shield_hp + 1)))
        self.space_shield.set_alpha(alpha)

    def space_shield_update(self, health):
        self.space_shield_hp += health
        if self.space_shield_hp > self.space_shield_max:
            self.space_shield_hp = self.space_shield_max
        elif self.space_shield_hp < 0:
            self.space_shield_hp = 0

        alpha = min(255, int(60 * log(self.space_shield_hp + 1)))
        self.space_shield.set_alpha(alpha)

    def set_regenerate(self, toggle, player=None, game=None):
        if self.regenerate and toggle and player and game:
            return False
        else:
            self.regenerate = toggle
            self.regenerated_blocks = 0
            self.regen_safe = 0
            return True

    def set_position(self, *args):
        super().set_position(*args)
        self.position_blocks()

    def update(self, game):
        super().update(game)

        if self.space_shield_max > 0 and self.tick % self.space_shield_cd == 0:
            self.space_shield_update(1)

        cd_multi = 1
        if self.layers_filled[0]: cd_multi += 0.2
        if self.layers_filled[1]: cd_multi += 0.1

        if self.regenerate:
            self.regen_safe += 1
            if self.tick % self.regen_cd * cd_multi == 0:
                self.heal(game, 1)
                self.regenerated_blocks += 1
            if self.regenerated_blocks >= self.max_blocks_regen:
                self.set_regenerate(False)

    def draw(self, game):
        super().draw(game)

        if self.blink or (not self.got_inside and not self.visible):
            for block in self.blocks:
                block.draw(game)

        if not self.visible:
            game.screen.blit(self.space_shield, self.space_shield_rect)

        if self.tick % self.pointer_cd == 0:
            self.pointer_pos = -self.pointer_pos
            new_y = self.size[1] // 2 + self.pointer_pos
            self.pointer.set_position(self.rect.centerx, self.rect.centery - new_y)

        if self.visible and self.can_get_in:
            self.pointer.draw(game)
