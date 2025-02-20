import pygame as pg
from random import randint, choice

class Poison:
    def __init__(self, position, size, color=(255, 255, 255), alpha=160):
        self.type = 'poison'
        self.size = [size // 4, size // 4]
        self.color = color
        self.sprite = pg.image.load(f'assets/bullet_sprites/puddle.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.size[0], self.size[1]))
        self.sprite = pg.transform.rotate(self.sprite, choice([90, 180, 270, 360]))

        self.rect = self.sprite.get_rect()
        self.rect.center = position
        self.base_center = position
        self.life_tick = 0
        self.max_lifetick = 1200
        self.alive = True

        self.spread_count = 0
        self.spread_max = 8
        self.spread_time = 15
        self.size_add = size // choice([1.5, 1.6, 1.7, 1.8, 1.9, 2])
        self.alpha = alpha

        self.sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        self.sprite.set_alpha(alpha)

    def set_values(self, max_lifetime, spread_max, spread_time, size_add):
        self.max_lifetick = max_lifetime
        self.spread_max = spread_max
        self.spread_time = spread_time
        self.size_add = size_add

    def update(self, game):
        self.life_tick += 1

        if self.life_tick >= self.max_lifetick:
            self.alive = False

        if self.life_tick >= self.max_lifetick - 240 and self.life_tick % self.spread_time == 0:
            self.alpha -= self.spread_time
            if not self.alpha <= 0:
                self.sprite.set_alpha(self.alpha)

        if self.life_tick % self.spread_time == 0 and self.spread_count < self.spread_max:
            # Increasing the size of the puddle
            self.size[0] += self.size_add // 1.5
            self.size[1] += self.size_add // 2

            # Creating a toxic puddle to trouble player
            self.spread_count += 1
            self.sprite = pg.transform.scale(self.sprite, (self.size[0], self.size[1]))
            self.rect = self.sprite.get_rect()
            self.rect.size = (self.size[0], self.size[1])
            self.rect.center = self.base_center

        self.collide_check(game)

    def collide_player(self, game, player):
        if self.rect.colliderect(player.hitbox):
            player.damage(game)

    def collide_check(self, game):
        if self.alive:
            # Checking collision with many different modules
            if game.player_1: self.collide_player(game, game.player_1)
            if game.player_2: self.collide_player(game, game.player_2)

    def draw(self, game):
        if self.alive:
            game.screen.blit(self.sprite, self.rect)
