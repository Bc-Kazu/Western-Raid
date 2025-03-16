"""
Class for player(s) functionalities, so we can make multiple players
with their own properties.
"""
from random import randint
from math import log

from constants import BASE_SHIELD_X, BASE_SHIELD_Y, BASE_PLAYER_SPEED, SHIELD_DISTANCE
from configurations.pickup_config import POWER_UPS, ITEMS, BRICKS
from assets import PLAYER_CONFIG, GADGET_CONFIG
from components.game_object import GameObject
import pygame as pg

from utils.colors import Colors

colors = Colors()

def load_player_sprite(player, name):
    image = pg.image.load(f'assets/player_sprites/{player.id}/{name}.png')
    image = pg.transform.scale(image, player.size)

    if 'eyes' in name:
        player.eyes_dict[name] = image
    return image

class Player(GameObject):
    # Define a dictionary that maps control types to their respective key mappings
    CONTROL_MAPPING = {
        'WASD': {'left': pg.K_a, 'right': pg.K_d, 'down': pg.K_s, 'up': pg.K_w},
        'ARROWS': {'left': pg.K_LEFT, 'right': pg.K_RIGHT, 'down': pg.K_DOWN, 'up': pg.K_UP}
    }

    def __init__(self, choosen_controls, player_count, color):
        super().__init__(PLAYER_CONFIG, player_count)
        self.type = 'player'
        self.controls = choosen_controls
        self.color = color
        self.current_eyes = None
        self.eyes_dict = {}
        self.key_mapping = self.CONTROL_MAPPING[self.controls]
        self.control_keys = self.key_mapping.values()

        self.sprite = load_player_sprite(self, 'body')
        self.base_eyes = load_player_sprite(self, 'base_eyes')
        self.happy_eyes = load_player_sprite(self, 'happy_eyes')
        self.closed_eyes = load_player_sprite(self, 'closed_eyes')
        self.shock_eyes = load_player_sprite(self, 'shock_eyes')
        self.angry_eyes = load_player_sprite(self, 'angry_eyes')
        self.squint_eyes = load_player_sprite(self, 'squint_eyes')
        self.current_eyes = self.base_eyes
        self.config['image'] = self.sprite.copy()

        self.outline = pg.image.load(f'assets/player_sprites/{self.id}/outline.png')
        self.outline = pg.transform.scale(self.outline, (self.size[0] + 4, self.size[1] + 4))
        self.outline_rect = self.outline.get_rect()

        # Creating hitbox with smaller size and accurate position to the player sprite
        self.hitbox_area = pg.Surface((int(self.size[0] * 0.8), self.size[1] // 2), pg.SRCALPHA)
        self.hitbox_area.fill(colors.yellow)
        self.hitbox_area.set_alpha(150)
        self.hitbox = self.hitbox_area.get_rect()

        # Player's shield
        self.shield_x = SHIELD_DISTANCE if self.id == 2 else -SHIELD_DISTANCE
        self.shield_y = 0
        self.shield_width = BASE_SHIELD_Y
        self.shield_height = BASE_SHIELD_X
        self.shield_rect = pg.Rect(0, 0, self.shield_width, self.shield_height)
        self.shield_rect.topleft = self.rect.topleft

        # Player values
        self.score = 0
        self.speed = BASE_PLAYER_SPEED
        self.shield_tick = 0
        self.shield_cooldown = 150
        self.push_power = 15
        self.shoot_cooldown = 100
        self.holding = None

        self.super_color_list = [colors.yellow, colors.cyan]
        self.set_color(colors.black, self.outline)
        self.super_color_shift = False
        self.super_color_tick = 0
        self.super_color_interval = 5
        self.super_color_index = 0

        self.victory_tick = 0
        self.victory_cooldown = 60

        self.recovery_tick = 0
        self.recovery_cd = 100

        self.alive = True
        self.shield_visible = True
        self.stay_within_screen = True
        self.facing_up = False
        self.last_key = ''
        self.last_direction = [0, 0]
        self.rect_offset = [0, 0]
        self.eyes_offset = [0, 0]

        # Value for the number of times an input has been pressed
        self.keys_pressed = 0

        # Dictionary list for power-ups the player will collect
        self.PU_list = {}

        # Special buff values
        self.shield_buff = pg.Surface((int(self.size[0] * 1.2), int(self.size[0] * 1.2)), pg.SRCALPHA)
        self.shield_buff.fill(colors.light_blue)
        self.shield_buff.set_alpha(0)
        self.shield_buff_hp = 0

    def super_effect(self):
        if self.super_color_shift and self.super_color_tick % self.super_color_interval == 0:
            self.super_color_index += 1
            if self.super_color_index > len(self.super_color_list) - 1:
                self.super_color_index = 0

            new_color = self.super_color_list[self.super_color_index]
            self.set_color(new_color, self.outline)

    def set_super(self):
        self.super_color_shift = not self.super_color_shift

        if not self.super_color_shift:
            self.set_color(colors.white, self.outline)

    def get_powerup(self, game, power_up):
        heal = False
        pu_name = power_up.replace('_', ' ').upper()

        if power_up in self.PU_list:
            if self.PU_list[power_up] < POWER_UPS[power_up][2]:
                self.PU_list[power_up] += 1
                game.sound.play_sfx('powerup_get')
                game.level.spawn_message('popup', f'+{pu_name} PU', self.rect.center)
            else:
                self.get_score(game, POWER_UPS[power_up][3], True, self.rect.center)
                game.sound.play_sfx('points')
                game.sound.play_sfx('points_extra')
        else:
            self.PU_list[power_up] = 1
            game.sound.play_sfx('powerup_get')
            game.level.spawn_message('popup', f'+{pu_name} PU', self.rect.center)

            if power_up == 'space_shield':
                heal = True

        game.ufo.space_shield_set(game, heal)

    def get_item(self, game, item):
        item_got = False
        if item == 'shield':
            self.shield_buff_hp += 1
            item_got = self.shield_buff_hp <= ITEMS[item][2]
            if not item_got:
                self.shield_buff_hp = ITEMS[item][2]

            self.shield_buff.set_alpha(self.shield_buff_hp * 20)
        if item == 'healing_ufo':
            item_got = game.ufo.set_regenerate(True, self, game)
        if item in GADGET_CONFIG:
            item_got = game.level.spawn_gadget(game, item, self)

        if item_got:
            game.sound.play_sfx('item_get')
        else:
            game.sound.play_sfx('points')
            self.get_score(game, ITEMS[item][3], True, self.rect.center)

    def get_score(self, game, amount, has_popup=False, popup_rect=None):
        new_amount = int(amount) if not game.player_2 else int(amount // 2)
        self.score += new_amount

        if has_popup and popup_rect:
            game.level.spawn_message('popup', f'+{new_amount}', popup_rect)

    # Handle player behaviour depending on direction given
    # The self.last_key conditions allows the shield to not break on diagonal movement
    def change_direction(self, direction):
        shield_increment_x = 15 * self.PU_list.get('shield_size', 0)
        shield_increment_y = 2 * self.PU_list.get('shield_size', 0)
        speed_increment = 2 * self.PU_list.get('ghost_fury', 0) if not self.alive else 0

        if direction == 'left':
            self.velocity_x = -(self.speed + speed_increment)
            self.last_direction[0] = -2

            if self.last_key != 'up' and self.last_key != 'down':
                self.shield_y = 0
                self.shield_width = BASE_SHIELD_Y + shield_increment_y
                self.shield_height = BASE_SHIELD_X + shield_increment_x
                self.last_direction[1] = 0
            self.eyes_offset = [-4, 0]
            self.shield_x = -SHIELD_DISTANCE
        if direction == 'right':
            self.velocity_x = self.speed + speed_increment
            self.last_direction[0] = 2

            if self.last_key != 'up' and self.last_key != 'down':
                self.shield_y = 0
                self.shield_width = BASE_SHIELD_Y + shield_increment_y
                self.shield_height = BASE_SHIELD_X + shield_increment_x
                self.last_direction[1] = 0
            self.eyes_offset = [4, 0]
            self.shield_x = SHIELD_DISTANCE
        if direction == 'down':
            self.velocity_y = self.speed + speed_increment
            self.last_direction[1] = 2

            if self.last_key == 'left' or self.last_key == 'right':
                self.eyes_offset[1] = 4
            else:
                self.last_direction[0] = 0
                self.eyes_offset = [0, 4]
                self.shield_x = 0
                self.shield_width = BASE_SHIELD_X + shield_increment_x
                self.shield_height = BASE_SHIELD_Y + shield_increment_y
            self.shield_y = SHIELD_DISTANCE
        if direction == 'up':
            self.velocity_y = -(self.speed + speed_increment)
            self.last_direction[1] = -2

            if self.last_key == 'left' or self.last_key == 'right':
                self.eyes_offset[1] = -4
            else:
                self.last_direction[0] = 0
                self.facing_up = True
                self.shield_x = 0
                self.shield_width = BASE_SHIELD_X + shield_increment_x
                self.shield_height = BASE_SHIELD_Y + shield_increment_y
            self.shield_y = -SHIELD_DISTANCE
        else:
            self.facing_up = False

        self.last_key = direction

    # Handle controls and changing sprites (shield, eyes, etc.)
    def update(self, game):
        joining = False
        for player in game.joined_late:
            if player == self:
                joining = True

        if game.level and game.level.started and not joining:
            self.eyes_offset = [0, 0]
            self.set_velocity(0, 0)

            # Checking different keys depending on the current player controls
            for direction, key in self.key_mapping.items():
                if game.keys_pressed[key]:
                    self.change_direction(direction)

            if self.stuck:
                self.set_velocity(0, 0)

        super().update(game)

        # Update the shield rotation and position
        self.shield_rect.width = self.shield_width
        self.shield_rect.height = self.shield_height
        self.shield_rect.center = self.rect.center
        self.shield_rect.x += self.shield_x
        self.shield_rect.y += self.shield_y

        # Adjust hitbox position
        self.hitbox.center = (self.rect.centerx, self.rect.centery + self.size[1] // 4)

        # Allowing custom player bullet_sprites from power-up
        if 'auto_shoot' in self.PU_list and not game.level.victory:
            power = self.PU_list['auto_shoot']

            if 'ghost_fury' in self.PU_list and not self.alive:
                power += self.PU_list['ghost_fury']

            if self.tick % int((self.shoot_cooldown / power)) == 0:
                speed_x = self.last_direction[0] * log(power + 3)
                speed_y = self.last_direction[1] * log(power + 3)
                self.shoot(game, (speed_x, speed_y))
                game.sound.play_sfx('bandit_shoot')

                if 'extra_reflect' in self.PU_list:
                    chance = self.PU_list['extra_reflect'] * 18 > randint(1, 100)
                    if chance:
                        self.shoot(game, (-speed_x, -speed_y))

        if 'recovery' in self.PU_list:
            self.recovery_cd = 100 + 80 * self.PU_list['recovery']
            self.shield_cooldown = 150 - 15 * self.PU_list['recovery']

        # Applying shield cooldown timer
        if not self.alive:
            self.shield_tick += 1
            if self.shield_tick % self.shield_cooldown == 0:
                self.alive = True
                game.sound.play_sfx('recover')
        else:
            self.recovery_tick += 1

    def shoot(self, game, velocity):
        extra_size = 2 * self.PU_list.get('bullet_size', 0)

        new_bullet = game.bullet_pool_dict['bullet'].get()
        new_bullet.spawn(self.rect.center, velocity, self)
        size = (new_bullet.size[0] + extra_size, new_bullet.size[1] + extra_size)
        new_bullet.set_size(size)

        game.level.bullets.append(new_bullet)
        game.data[f"p{self.id}_stats"]["bullets_shot"] += 1

    def damage(self, game):
        if self.alive and self.recovery_tick >= self.recovery_cd:
            game.data[f"p{self.id}_stats"]["damaged"] += 1
            self.recovery_tick = 0

            if self.shield_buff_hp > 0:
                self.shield_buff_hp -= 1
                self.shield_buff.set_alpha(self.shield_buff_hp * 20)
                game.sound.play_sfx('shield_hit')
                return

            self.kill()
            self.shield_tick = 0
            game.sound.play_sfx('player_damage')
    
    def set_offset(self, rect_offset=None, eyes_offset=None):
        self.rect_offset = rect_offset
        self.eyes_offset = eyes_offset

    def set_eyes(self, name):
        self.current_eyes = self.eyes_dict[name]

    def draw(self, game):
        if game.scene.state and game.scene.state['name'] == 'init_cutscene':
            if game.scene.state['tick'] < game.scene.state['destroy_interval']:
                return

        if game.ufo.got_inside and not game.scene.name == 'victory':
            return

        # self.super_effect()
        if self.super_color_shift:
            self.super_color_tick += 1
            self.outline_rect.center = self.rect.center
            game.screen.blit(self.outline, self.outline_rect)

        super().draw(game)

        if game.scene.name == 'defeat':
            self.eyes_offset = [-2, 2] if self.id == 1 else [2, 2]
            self.alive = True

        if not self.facing_up:
            eyes_pos = (self.rect.x + self.eyes_offset[0], self.rect.y + self.eyes_offset[1])
            game.screen.blit(self.current_eyes, eyes_pos)

        # Conditions for certain things to be drawn
        if self.alive:
            self.current_eyes.set_alpha(255)
            self.sprite.set_alpha(255)
            self.outline.set_alpha(255)

            if game.scene.name == 'round':
                if not game.level.defeat and self.shield_visible:
                    pg.draw.rect(game.screen, self.color, self.shield_rect)

                if self.shield_buff_hp > 0:
                    shield_offset = int(self.size[0] / 1.65)
                    game.screen.blit(self.shield_buff, (self.rect.centerx - shield_offset,
                                                        self.rect.centery - shield_offset))
        elif game.scene.name == 'round':
            self.current_eyes.set_alpha(128)
            self.sprite.set_alpha(128)
            self.outline.set_alpha(128)

        if game.scene.name == 'defeat':
            self.rect.center = (game.screen_width / 2, game.screen_height - 160)
            self.facing_up = False
            if self.rect_offset:
                self.rect.x += self.rect_offset[0]
                self.rect.y += self.rect_offset[1]