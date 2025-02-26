import pygame as pg

class Explosion:
    def __init__(self, game, position, size, sound='explode'):
        self.type = 'explosion'
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = position
        self.life_tick = 0
        self.color_tick = 0
        self.max_lifetick = 40
        self.alive = True
        self.color = (255, 255, 255)
        self.explode_color1 = (255, 130, 0)
        self.explode_color2 = (255, 240, 0)

        self.ufo_collided = False
        self.already_hit = []    # List of objects that already got hit, to avoid multiple checks

        if sound:
            game.sound.play_sfx(sound)

    def set_lifetick(self, new_max):
        self.max_lifetick = new_max

    def set_color(self, color1=(255, 130, 0), color2=(255, 240, 0)):
        self.explode_color1 = color1
        self.explode_color2 = color2

    def update(self, game):
        self.life_tick += 1
        self.color_tick += 1
        self.collide_check(game)

        # Changing colors for explosion effect
        if self.color_tick >= 8 and self.color != self.explode_color1:
            self.color_tick = 0
            self.color = self.explode_color1
        elif self.color_tick >= 8 and self.color != self.explode_color2:
            self.color_tick = 0
            self.color = self.explode_color2

        if self.life_tick >= self.max_lifetick:
            self.alive = False
            self.already_hit = []

    def collide_player(self, game, player):
        if self.rect.colliderect(player.hitbox):
            player.damage(game)

    def collide_ufo(self, game):
        if not game.ufo.blocks:
            return

        # check the collides by the lists
        for block in game.ufo.blocks:
            # Checks if the bullet_sprites collides w ufo
            if self.rect.colliderect(block.rect) and block.strength >= 1:
                game.ufo.take_damage(game, block)

    def collide_check(self, game):
        if self.alive:
            # Checking collision with many different modules
            if game.player_1: self.collide_player(game, game.player_1)
            if game.player_2: self.collide_player(game, game.player_2)

            if not self.ufo_collided:
                self.ufo_collided = True
                self.collide_ufo(game)

            for obj in game.level.objects:
                if obj in self.already_hit:
                    continue

                if self.rect.colliderect(obj.rect) and obj.type == 'rope':
                    obj.kill()

                    if obj.alive:
                        self.already_hit.append(obj)

            for gadget in game.level.gadgets:
                if gadget in self.already_hit:
                    continue

                if self.rect.colliderect(gadget.rect):
                    if (not hasattr(gadget, "is_placed") or
                            (hasattr(gadget, "is_placed") and gadget.is_placed)):
                        gadget.damage(game, 3)
                        if gadget.alive:
                            self.already_hit.append(gadget)

            for terrain in game.level.map:
                if terrain in self.already_hit:
                    continue

                if self.rect.colliderect(terrain.rect):
                    terrain.destroy(game)

                    if terrain.alive:
                        self.already_hit.append(terrain)

            for bandit in game.level.bandits:
                if bandit in self.already_hit:
                    continue

                if self.rect.colliderect(bandit.rect):
                    bandit.damage(game, 3)

                    if bandit.alive:
                        self.already_hit.append(bandit)

            for bullet in game.level.bullets:
                if bullet in self.already_hit:
                    continue

                if self.rect.colliderect(bullet.rect):
                    bullet.kill()

    def draw(self, game):
        if self.alive:
            pg.draw.rect(game.screen, self.color, self.rect)
