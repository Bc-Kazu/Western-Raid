import pygame as pg
from random import randint, choice
from assets import LUCK_STATUE
from components.game_object import GameObject

from utils.colors import Colors
colors = Colors()

class Decoration:
    def __init__(self, name, size, position, color):
        self.name = name
        self.size = size
        self.sprite = pg.image.load(f'assets/decoration_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, self.size)
        self.sprite.fill(color, special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.sprite.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class Terrain(GameObject):
    def __init__(self, config, terrain_id, level):
        if randint(-777, 777) == 777:
            config = LUCK_STATUE

        super().__init__(config, terrain_id)
        self.area_rect = pg.Rect(self.rect.x, self.rect.y,
                                 self.size[0] / level.terrain_area_reduction,
                                 self.size[1] / level.terrain_area_reduction)
        self.area_rect.center = self.rect.center
        self.area_surface = pg.Surface(self.area_rect.size, pg.SRCALPHA)
        self.area_surface.fill(colors.orange)
        self.area_surface.set_alpha(40)
        self.decorations = []
        self.alive = True
        self.follow_strength = 1


    def set_decoration(self):
        if self.name == 'table':
            deco_amount = randint(0, 2)

            for deco in range(deco_amount):
                random_deco = choice([
                    ['small_bottle', (110, 110, 100)],
                    ['hat', (150, 150, 150)],
                    ['food', (120, 70, 20)],
                    ['chess', (120, 120, 120)],
                    ['dabloons', (150, 140, 80)]
                ])
                deco = Decoration(random_deco[0], self.size, self.rect, random_deco[1])
                self.decorations.append(deco)

            seats_amount = randint(0, 2)

            for seat in range(seats_amount):
                random_seat = ['chair', (100, 60, 65)]
                if randint(1, 10) == 1: random_seat = ['funny_chair', (100, 60, 65)]

                if seat == 1:
                    seat_pos = [self.rect.x - self.size[0] + 10, self.rect.y]
                else:
                    seat_pos = [self.rect.x + self.size[0]  - 10, self.rect.y]

                seat = Decoration(random_seat[0], self.size, seat_pos, random_seat[1])
                self.decorations.append(seat)
        if self.name == 'large_table':
            deco_amount = randint(1, 3)
            already_has = False

            for deco in range(deco_amount):
                random_deco = choice([
                    ['wasted_bandit', (150, 150, 150)],
                    ['small_bottle', (110, 110, 100)],
                    ['hat', (150, 150, 150)],
                    ['food', (120, 70, 20)],
                    ['chess', (120, 120, 120)],
                    ['dabloons', (150, 140, 80)]
                ])

                for existing in self.decorations:
                    if random_deco[0] == 'wasted_bandit' and existing.name == 'wasted_bandit':
                        already_has = True
                if already_has: continue

                if random_deco[0] == 'wasted_bandit':
                    new_size = (self.size[0] // 1.5, self.size[1] // 1.5)
                    pos_offset = (new_size[0] // 2.55, new_size[1] // 2.55)
                    deco = Decoration(random_deco[0], new_size,
                    [self.rect.x + randint(0, pos_offset[0]), self.rect.y + pos_offset[1]], random_deco[1])
                else:
                    new_size = (self.size[0] // 2, self.size[1] // 2)
                    deco = Decoration(random_deco[0], new_size,
                    [self.rect.x + randint(0, new_size[0]), self.rect.y + new_size[1]], random_deco[1])
                self.decorations.append(deco)

    def set_position(self, *args):
        super().set_position(args)
        self.area_rect.center = self.rect.center

    def distance_check(self, level):
        if self.area_rect.colliderect(level.ufo.rect):
            self.kill()
            return

        if self.name == 'luck_statue':
            return

        # Check if there are any terrain too close to the hitbox, and remove it
        for terrain in level.map:
            if self.area_rect.colliderect(terrain.area_rect) and terrain.id != self.id and terrain.alive:
                self.kill()
                break

    def destroy(self, game):
        if self.alive:
            self.kill()
            game.sound.play_sfx('remove')
            game.data["terrain_destroyed"] += 1

            if self.name == 'luck_statue':
                game.level.spawn_pickup('power_up', self.rect.center)
            elif randint(1, 4 + len(self.decorations)) >= randint(1, 4):
                game.level.spawn_pickup('brick', self.rect.center)


    def draw(self, game):
        self.area_rect.center = self.rect.center

        if game.debug:
            game.screen.blit(self.area_surface, self.area_rect)

        super().draw(game)

        for decoration in self.decorations:
            game.screen.blit(decoration.sprite, decoration.rect)
