from assets import TEXT_FONT

from components.game_object import GameObject
from utils.text import Text
from utils.colors import Colors
colors = Colors()

class Block(GameObject):
    def __init__(self, config, block_id=None):
        super().__init__(config, block_id)
        self.strength = 1
        self.row = 1
        self.strength_indicator = Text(str(self.strength), self.rect.center, TEXT_FONT, colors.strong_shadow)

    def set_strength(self, value, change_color=True):
        self.strength = value
        if self.strength < 0:
            self.strength = 0

        self.strength_indicator.set_text(str(self.strength))

        if change_color:
            self.set_color()

    def set_color(self, custom=None, custom_sprite=None):
        if self.strength == 0:
            self.color = colors.window_crimson
            if 'broken_image' in self.config:
                self.sprite = self.config['broken_image'].copy()
                self.set_size(self.size)
        else:
            if self.strength == 1 and 'image' in self.config:
                self.sprite = self.config['image'].copy()
                self.set_size(self.size)

            if hasattr(self.owner, 'block_colors'):
                new_colors = self.owner.block_colors
                color_pallete = len(new_colors[0])

                if self.row < color_pallete:
                    self.color = new_colors[self.strength - 1][self.row]
                else:
                    self.color = new_colors[self.strength - 1][color_pallete - 1]
            else:
                self.color = self.owner.color

        super().set_color(custom, custom_sprite)

    def collide_check(self, bullet):
        # Checks if the bullet_sprites collides w ufo
        if (self.rect.colliderect(bullet.rect) and bullet.owner.type == 'enemy'
                and self.strength >= 1 and bullet.alive):
            bullet.kill()
            if self.can_die: self.kill()
            return True
        else:
            return False

    def draw(self, game):
        super().draw(game)

        if game.debug:
            self.strength_indicator.draw(game)