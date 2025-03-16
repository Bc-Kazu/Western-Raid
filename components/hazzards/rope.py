import pygame as pg
from math import degrees, atan2

from assets import BULLET_CACHE
from utils.colors import Colors
colors = Colors()

class Rope:
    def __init__(self, game, starter_pos, distance, size, owner=None):
        self.type = 'rope'
        self.color = colors.saddle_brown
        self.sprite = BULLET_CACHE['bullet'].copy()
        self.sprite = pg.transform.scale(self.sprite, size)
        rope_angle = degrees(atan2(distance[0], distance[1]))
        self.sprite = pg.transform.rotate(self.sprite, (int(rope_angle) + 90))
        self.sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        self.hitbox_list = []

        rect_factor = 0.1
        while rect_factor <= 1:
            new_rect = pg.Rect(starter_pos,(size[1], size[1]))
            new_rect.center = starter_pos
            new_rect.x += distance[0] * rect_factor
            new_rect.y += distance[1] * rect_factor
            self.hitbox_list.append(new_rect)
            rect_factor += 0.1

        self.rect = self.sprite.get_rect(center=starter_pos)
        self.rect.center = (starter_pos[0] + distance[0] // 2, starter_pos[1] + distance[1] // 2)
        self.health = 15
        self.tick = 0
        self.max_lifetick = 60
        self.enabled = True
        self.alive = True
        self.owner = owner

        self.wrapped_rope = BULLET_CACHE['wrapped_rope'].copy()
        self.wrapped_rope_rect = self.wrapped_rope.get_rect()
        self.wrapped_lifetick = 300

        self.hit = False
        self.enrolled_target = None

        game.sound.play_sfx('rope')

    def kill(self):
        self.alive = False
        if self.enrolled_target:
            self.enrolled_target.stuck = False

    def set_lifetick(self, new_max):
        self.max_lifetick = new_max

    def damage(self, game, damage):
        if self.alive:
            game.sound.play_sfx('push')
            self.health = max(0, self.health - damage)
            new_alpha = self.health * 15 if self.health * 15 < 255 else 255
            self.wrapped_rope.set_alpha(new_alpha)
            if self.health < 1:
                game.sound.play_sfx('remove')
                self.kill()

    def update(self, game):
        self.tick += 1
        self.collide_check(game)

        if self.enrolled_target and self.enrolled_target.type == 'player':
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in self.enrolled_target.control_keys:
                        self.damage(game, 1)


        if self.tick >= self.max_lifetick:
            self.enabled = False
        if self.tick >= self.wrapped_lifetick:
            self.kill()

    def enroll(self, game, target):
        if not target.stuck:
            self.wrapped_rope = BULLET_CACHE['wrapped_rope'].copy()
            self.wrapped_rope = pg.transform.scale(self.wrapped_rope, target.size)

            self.wrapped_rope.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
            self.wrapped_rope_rect = self.wrapped_rope.get_rect()
            self.wrapped_rope_rect.center = target.rect.center
            self.hit = True
            self.enrolled_target = target
            self.enabled = False
            target.stuck = True
            game.sound.play_sfx('stuck')

            if self.owner:
                self.owner.on_rope_hit()

    def collide_player(self, game, player):
        for rect in self.hitbox_list:
            if rect.colliderect(player.hitbox):
                self.enroll(game, player)
                return

    def collide_check(self, game):
        if self.alive and self.enabled and not self.hit:
            # Checking collision with many different modules
            if game.player_1:
                self.collide_player(game, game.player_1)
                if self.hit: return
            if game.player_2:
                self.collide_player(game, game.player_2)
                if self.hit: return

            for bandit in game.level.bandits:
                if self.owner and bandit == self.owner:
                    continue

                for rect in self.hitbox_list:
                    if rect.colliderect(bandit.rect):
                        self.enroll(game, bandit)
                        return

            for gadget in game.level.gadgets:
                for rect in self.hitbox_list:
                    if rect.colliderect(gadget.rect):
                        if (not hasattr(gadget, "is_placed") or
                                (hasattr(gadget, "is_placed") and gadget.is_placed)):
                            self.enroll(game, gadget)
                        return

        elif self.enrolled_target:
            if self.wrapped_rope_rect.colliderect(self.enrolled_target.rect):
                new_center = self.enrolled_target.rect.center
                new_center = (new_center[0], new_center[1] + 8)
                self.wrapped_rope_rect.center = new_center

    def draw(self, game):
        if self.alive and self.enabled:
            game.screen.blit(self.sprite, self.rect)

            if game.debug:
                for rect in self.hitbox_list:
                    pg.draw.rect(game.screen, colors.red, rect)
        if self.enrolled_target:
            game.screen.blit(self.wrapped_rope, self.wrapped_rope_rect)
