import pygame as pg
from components.objects.bandit_model import BanditModel
from assets import BULLET_CACHE
from utils.colors import Colors
colors = Colors()

class Bandit(BanditModel):
    def __init__(self, config, bandit_id):
        super().__init__(config, bandit_id)
        self.base_shoot_interval = 400
        self.move_range = 150
        self.base_drop_chances = {'power_up': 10, 'item': 20, 'brick': 100}
        self.points_value = 40
        self.move_interval_base = [500, 1200]
        self.shield_enabled = True

        # Table or shielded bandit values
        self.shield = BULLET_CACHE['center_table'].copy()
        self.shield = pg.transform.scale(self.shield, (100, 100))
        self.shield = pg.transform.rotate(self.shield, -90)
        self.shield.fill(colors.saddle_brown, special_flags=pg.BLEND_RGBA_MULT)
        self.shield_rect = self.shield.get_rect()
        self.shield_hitbox = pg.Rect(self.shield_rect.x, self.shield_rect.y, 60, 100)
        self.shield_health = 3

    def update(self, game):
        super().update(game)

        # Choosing the side position and rotation depending on left_hand or right on screen
        left_distance = [[self.size[0], 0], -180, 0 + self.rect.x]
        right_distance = [[-self.size[0], 0], 180, game.screen_width - self.rect.x]
        smallest_x = min(left_distance[2], right_distance[2])

        side_goal = left_distance if smallest_x == left_distance[2] else right_distance

        if self.last_side != side_goal[0]:
            self.shield = pg.transform.rotate(self.shield, side_goal[1])

        # Updating position relative to bandit
        self.shield_rect.center = self.rect.center
        self.shield_rect.x += side_goal[0][0]
        self.shield_rect.y += side_goal[0][1]
        self.shield_hitbox.center = self.shield_rect.center
        self.last_side = side_goal[0]

        if self.shield_health <= 0 and self.shield_enabled:
            self.shield_enabled = False
            self.base_shoot_interval = 180
            self.points_value = 50
            self.move_interval_range = [180, 900]

        self.shield_check(game)

    def shield_check(self, game):
        for bullet in game.level.bullets:
            if bullet.owner.type != 'player':
                continue
            elif bullet.rect.colliderect(self.shield_hitbox) and self.shield_enabled:
                # Get the relative position of the collision
                self.shield_health -= 1
                self.shield.fill(colors.tan, special_flags=pg.BLEND_RGBA_MULT)
                game.sound.play_sfx('shield_hit')

                # Convert bullet's ownership to the bandit
                bullet.set_owner(self)
                bullet.reflect(self.shield_hitbox, None, game)

                if self.shield_health <= 0:
                    game.sound.play_sfx('bandit_damage')

    def draw(self, game):
        super().draw(game)
        if self.shield_enabled:
            game.screen.blit(self.shield, self.shield_rect)