"""
Class made to handle managing text and applying effects or changes
"""
import pygame.transform as transform

class Text:
    def __init__(self, text, rect, font, base_color=(255, 255, 255)):
        self.type = 'text'
        self.style = 'base'
        self.string = text
        self.rect = rect
        self.velocity_x = 0
        self.velocity_y = 0
        self.font = font
        self.enabled = True
        self.visible = True

        self.alive = True
        self.tick = 0
        self.max_lifetick = 0

        # Visual effects for text
        self.blink = False
        self.color_blink = False
        self.background = False

        self.base_color = base_color
        self.current_color = self.base_color
        self.blink_color = (255, 255, 240)
        self.background_color = (0, 0, 0)

        self.icon = None
        self.icon_size = 50
        self.icon_offset = (0, 0)

        self.blink_tick = 0
        self.blink_interval = 15

    def preset(self, style='base', velocity=(0, 0), lifetick=0):
        self.style = style
        self.set_velocity(velocity)
        self.max_lifetick = lifetick

    def toggle(self, enable):
        self.enabled = enable

    def set_blink(self, blink, interval=None):
        self.blink = blink
        if interval: self.blink_interval = interval

    def set_color_blink(self, color_blink, color=None, interval=None):
        self.color_blink = color_blink
        if color: self.blink_color = color
        if interval: self.blink_interval = interval

    def set_background(self, enable, color=None):
        self.background = enable
        if color: self.background_color = color

    def set_icon(self, icon=None, icon_size=None, icon_offset=None):
        if icon: self.icon = icon
        if icon_size:
            self.icon_size = icon_size
            self.icon = transform.scale(self.icon, (icon_size, icon_size))
        if icon_offset: self.icon_offset = icon_offset

    def set_text(self, new_text):
        self.string = new_text

    # Sets the X and Y velocity vectors for the object.
    # Allows tuple, lists or both values separately as arguments.
    def set_velocity(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            self.velocity_x = args[0][0]
            self.velocity_y = args[0][1]
        elif len(args) == 2:
            self.velocity_x = args[0]
            self.velocity_y = args[1]

    def set_position(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.rect = args[0]
        elif len(args) == 2:
            self.rect = (args[0], args[1])

    def set_font(self, new_font):
        self.font = new_font

    def set_color(self, new_color=None):
        if new_color:
            self.current_color = new_color
        else:
            self.current_color = self.base_color

    def blink_text(self):
        if not self.enabled: return

        # Visibility blinking check
        if self.blink and self.blink_tick >= self.blink_interval:
            self.visible = not self.visible
            self.blink_tick = 0

        # Color blinking check
        if self.color_blink and self.blink_tick >= self.blink_interval:
            self.blink_tick = 0
            if self.current_color != self.blink_color:
                self.current_color = self.blink_color
            else:
                self.current_color = self.base_color

    def update(self, game):
        self.tick += 1
        self.rect = (self.rect[0] + self.velocity_x, self.rect[1] + self.velocity_y)

        if 0 < self.max_lifetick < self.tick:
            self.alive = False

    def draw(self, game=None, custom_screen=None):
        self.blink_tick += 1
        self.blink_text()

        if self.enabled and self.visible:
            # Applying built-in background for text is enabled
            if self.background:
                render_text = self.font.render(self.string, True, self.current_color, self.background_color)
            else:
                render_text = self.font.render(self.string, True, self.current_color)

            if len(self.base_color) > 3:
                render_text.convert_alpha()
                render_text.set_alpha(self.base_color[3])

            if self.icon:
                icon_rect = (self.rect[0] - self.icon_size + self.icon_offset[0],
                             self.rect[1] + self.icon_offset[1])

                if game:
                    game.screen.blit(self.icon, icon_rect)
                if not game and custom_screen:
                    custom_screen.blit(self.icon, icon_rect)

            if game:
                if isinstance(self.rect, tuple):
                    game.screen.blit(render_text, render_text.get_rect(center=self.rect))
                else:
                    game.screen.blit(render_text, render_text.get_rect(self.rect))
            if not game and custom_screen:
                if isinstance(self.rect, tuple):
                    custom_screen.blit(render_text, render_text.get_rect(center=self.rect))
                else:
                    custom_screen.blit(render_text, render_text.get_rect(self.rect))