import pygame
import pygame as pg
from random import randint

class SpawnParticle:
    def __init__(self, image=None, size=None, position=None, color=None, rotation=None):
        if position is None: position = [0, 0]
        if size is None: size = [8, 8]
        if color is None: color = (255, 255, 255, 255)
        if rotation is None: rotation = 0
        self.sprite = None
        self.surface = None
        self.rect = None
        self.size = size
        self.color = color
        self.rotation = rotation

        if image:
            self.sprite = pg.image.load(f'assets/particle_sprites/{image}.png').convert_alpha()
            self.sprite = pg.transform.scale(self.sprite, (self.size[0], self.size[1]))
            self.sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
            if self.rotation != 0:
                self.sprite = pg.transform.rotate(self.sprite, self.rotation)

            self.rect = self.sprite.get_rect()
            self.rect.center = position
        else:
            self.surface = pg.Surface((size[0], size[1]), pygame.SRCALPHA)
            self.rect = self.surface.get_rect()
            self.rect.center = position

        self.direction =  [randint(1, 3), 0]
        self.max_lifetime = 5
        self.lifetime = 0
        self.fade = [True, 1, 5]
        self.fade_check = False
        self.base_alpha = color[3]
        self.alive = True

    def update(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        if self.lifetime > self.max_lifetime: self.alive = False

        if self.fade[0]:
            if not self.fade_check:
                self.fade_check = True
                r, g, b, a = self.color
                a = 0
                self.color = (r, g, b, a)

            if self.lifetime <= self.fade[1]:
                r, g, b, a = self.color

                if a < self.base_alpha: a += self.fade[2]
                if a > self.base_alpha: a = self.base_alpha
                self.color = (r, g, b, a)
            elif self.lifetime >= self.max_lifetime - self.fade[1]:
                r, g, b, a = self.color

                if a > 0: a -= self.fade[2]
                if a < 0: a = 0
                self.color = (r, g, b, a)

    def draw(self, game):
        if not self.sprite:
            pg.draw.rect(self.surface, self.color, self.rect)
            self.surface.fill(self.color)
            game.screen.blit(self.surface, self.rect)
        else:
            r, g, b, a = self.color
            current_alpha = self.sprite.get_alpha()
            if a != current_alpha: self.sprite.set_alpha(a)

            game.screen.blit(self.sprite, self.rect)

class ParticleEmitter:
    def __init__(self, image=None, base_color=(255, 255, 255, 255)):
        self.image = image
        self.spawn_type = 'screen'
        self.base_color = base_color
        self.position = [0, 0]  # Position of the emitter rectangle, not the particle
        self.emitter_size = [0, 0]  # Size of the emitter rectangle, not the particle
        self.particles = []
        self.enabled = True

        # Size and direction uses min-max values for randomization [min, max]
        self.lifetime = [8, 16]
        self.size = [6, 12]
        self.direction_x = [1, 3]
        self.direction_y = [0, 0]
        self.base_rotation = [0, 0]

        # Values for random positions to spawn if spawn_type is 'screen'
        self.screen_posx = [-200, 960 - 400]
        self.screen_posy = [0, 620]

        # Emission values for the particles
        self.rate = 5
        self.spread = [0, 0]
        self.fading = [True, 1, 5]
        self.random_color = [False, False, 30]
        self.random_alpha = [False, 30]

    def emit(self):
        if not self.enabled: return

        # Applying randomization if values are different,
        # make both equal if you with for the same result (Ex: [5, 5])
        random_lifetime = randint(self.lifetime[0], self.lifetime[1])
        random_size = randint(self.size[0], self.size[1])
        random_rotation = randint(self.base_rotation[0], self.base_rotation[1])
        random_direction = [
            randint(self.direction_x[0], self.direction_x[1]),
            randint(self.direction_y[0], self.direction_y[1])
        ]

        size = [random_size, random_size]
        color = self.base_color
        new_particle = None

        if self.random_color[0]:
            if self.random_color[1]:
                r, g, b, a = color
                highest_value = max(r, g, b)
                rgb_new = randint(highest_value - self.random_color[2], highest_value + self.random_color[2])
                if rgb_new < 0: rgb_new = 0
                if rgb_new > 255: rgb_new = 255

                color = (rgb_new, rgb_new, rgb_new, a)
            else:
                r, g, b, a = color
                r_new = randint(r - self.random_color[2], r + self.random_color[2])
                g_new = randint(r - self.random_color[2], r + self.random_color[2])
                b_new = randint(r - self.random_color[2], r + self.random_color[2])
                if r_new < 0: r_new = 0
                if r_new > 255: r_new = 255
                if g_new < 0: g_new = 0
                if g_new > 255: g_new = 255
                if b_new < 0: b_new = 0
                if b_new > 255: b_new = 255

                color = (r_new, g_new, b_new, a)

        if self.random_alpha[0]:
            r, g, b, a = color
            a_new = randint(a - self.random_alpha[1], a + self.random_alpha[1])
            if a_new < 0: a_new = 0
            if a_new > 255: a_new = 255

            color = (r, g, b, a_new)

        if self.spawn_type == 'screen':
            random_pos = (randint(self.screen_posx[0], self.screen_posx[1]),
                          randint(self.screen_posy[0], self.screen_posy[1]))
            new_particle = SpawnParticle(self.image, size, random_pos, color, random_rotation)

        if new_particle:
            if self.fading[0]: new_particle.fade = self.fading
            new_particle.direction = random_direction
            new_particle.max_lifetime = random_lifetime
            self.particles.append(new_particle)

    def update(self, game):
        if not self.enabled: return
        time_frame = int(game.FPS / self.rate)
        time_frame = time_frame if time_frame >= 1 else 1

        if game.tick % time_frame == 0:
            self.emit()

        for particle in self.particles:
            particle.update()
            particle.draw(game)

            if game.tick % game.FPS == 0:
                particle.lifetime += 1
            if not particle.alive: self.particles.remove(particle)