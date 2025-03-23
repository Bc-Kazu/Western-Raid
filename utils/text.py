"""
Class made to handle managing text and applying effects or changes
"""
import pygame.transform as transform

class Text:
    def __init__(self, text, pos, font, base_color=(255, 255, 255)):
        self.type = 'text'
        self.style = 'base'
        self.string = text
        self.text = font.render(self.string, True, base_color)
        self.rect = self.text.get_rect()
        self.rect.center = pos
        self.velocity_x = 0
        self.velocity_y = 0
        self.font = font
        self.enabled = True
        self.visible = True

        self.alive = True
        self.tick = 0
        self.max_lifetick = 0
        self.stay_within_screen = False
        self.centered = True

        # Visual effects for text
        self.blink = False
        self.color_blink = False
        self.background = False

        self.base_color = base_color
        self.current_color = self.base_color
        self.blink_color = (255, 255, 240)
        self.blink_color2 = self.base_color
        self.background_color = (0, 0, 0)
        self.alpha = 255

        if len(self.current_color) > 3:
            self.alpha = self.current_color[3]

        self.icon = None
        self.icon_size = 50
        self.icon_rect = None
        self.icon_offset = (0, 0)

        self.blink_tick = 0
        self.blink_interval = 15
        self.rect_offset = [0, 0]

        self.update_text()

    def update_text(self):
        if self.background:
            self.text = self.font.render(self.string, True, self.current_color, self.background_color)
        else:
            self.text = self.font.render(self.string, True, self.current_color)

        new_rect = self.text.get_rect()
        new_rect.center = self.rect.center
        self.rect = new_rect

        if self.alpha < 255:
            self.text.convert_alpha()
            self.text.set_alpha(self.alpha)

        if self.icon:
            self.icon_rect = (self.rect.x - self.icon_size + self.icon_offset[0],
                         self.rect.centery + self.icon_offset[1])

    def preset(self, style='base', velocity=(0, 0), lifetick=0):
        self.style = style
        self.set_velocity(velocity)
        self.max_lifetick = lifetick
        self.stay_within_screen = True

    def toggle(self, enable):
        self.enabled = enable

    def set_centered(self, toggle):
        self.centered = toggle
        self.update_text()

    def set_blink(self, blink, interval=None):
        self.blink = blink
        if interval: self.blink_interval = interval

    def set_offset(self, *args):
        if len(args) == 0:
            self.rect_offset = [0, 0]
        elif len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.rect_offset = list(args[0])
        elif len(args) == 2:
            self.rect_offset[0] = args[0]
            self.rect_offset[1] = args[1]

        self.update_text()

    def set_offset_x(self, x=0):
        self.rect_offset[0] = x
        self.update_text()

    def set_offset_y(self, y=0):
        self.rect_offset[1] = y
        self.update_text()

    def set_color_blink(self, color_blink, interval=None, color=None, color2=None):
        self.color_blink = color_blink
        if color: self.blink_color = color
        if color2: self.blink_color2 = color2
        if interval: self.blink_interval = interval

    def set_background(self, enable, color=None):
        self.background = enable
        if color: self.background_color = color
        self.update_text()

    def set_icon(self, icon=None, icon_size=None, icon_offset=None):
        if icon: self.icon = icon
        if icon_size:
            self.icon_size = icon_size
            self.icon = transform.scale(self.icon, (icon_size, icon_size))
        if icon_offset: self.icon_offset = icon_offset
        self.update_text()

    def set_text(self, new_text):
        self.string = new_text
        self.update_text()

    # Sets the X and Y velocity vectors for the object.
    # Allows tuple, lists or both values separately as arguments.
    def set_velocity(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            self.velocity_x = args[0][0]
            self.velocity_y = args[0][1]
        elif len(args) == 2:
            self.velocity_x = args[0]
            self.velocity_y = args[1]

        self.update_text()

    def set_position(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            if self.centered:
                self.rect.center = args[0]
            else:
                self.rect.x = args[0][0]
                self.rect.centery = args[0][1]
        elif len(args) == 2:
            if self.centered:
                self.rect.center = (args[0], args[1])
            else:
                self.rect.x = args[0]
                self.rect.centery = args[1]


        self.update_text()

    def set_font(self, new_font):
        self.font = new_font
        self.update_text()

    def set_alpha(self, alpha):
        alpha = 255 if alpha > 255 else alpha
        alpha = 0 if alpha < 0 else alpha
        self.alpha = alpha
        self.update_text()

    def set_color(self, new_color=None):
        new_color = new_color if new_color else self.base_color
        self.current_color = new_color

        if len(self.current_color) > 3:
            self.set_alpha(self.current_color[3])

        self.update_text()

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
                self.current_color = self.blink_color2
            self.update_text()

    def update(self, game):
        self.tick += 1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if 0 < self.max_lifetick < self.tick:
            self.alive = False

    def draw(self, game=None, custom_screen=None):
        self.blink_tick += 1
        self.blink_text()
        screen = game.screen if game else custom_screen
        if not screen:
            return

        if game and self.stay_within_screen:
            # Making sure the object stays on screen
            self.rect.clamp_ip(game.screen_limit)

        if self.icon:
            screen.blit(self.icon, self.icon_rect)

        if self.enabled and self.visible:
            # Applying built-in background for text is enabled
            new_rect = (self.rect.x + self.rect_offset[0], self.rect.y + self.rect_offset[1])
            screen.blit(self.text, new_rect)