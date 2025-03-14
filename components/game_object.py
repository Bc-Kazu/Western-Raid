"""
GameObject class is made to serve other classes that identify as objects,
it holds many functions that a basic object would need specified for Western Raid
"""
import pygame as pg
import math

class GameObject:
    def __init__(self, config=None, obj_id=None):
        # Needs a basic image file if none is given, add the path of the file to load it here.
        self.NIL_IMAGE = pg.image.load('assets/nil.png').convert()

        # Basic attributes
        if config is None: config = {}
        self.id = obj_id
        self.config = config.copy()
        self.type = config.get('type', 'base_object')
        self.name = config.get('name', 'nil')
        self.color = config.get('color', (255, 255, 255))
        self.base_size = config.get('size', (50, 50))
        self.size = self.base_size
        self.spawnpoint = (0, 0)

        # Ownership attributes
        self.owner = None   # Owner is the parent that is currently holds ownership of the object
        self.spawner = None     # Spawner is the parent that first added it

        # Sprite and rect attributes
        self.sprite = config.get('image', self.NIL_IMAGE).copy()
        self.sprite = pg.transform.scale(self.sprite, self.size)
        self.rect = self.sprite.get_rect()

        # Object state attributes
        self.alive = False
        self.visible = True
        self.can_collide = True
        self.can_touch = True
        self.can_push = False
        self.can_die = True
        self.can_move = True

        self.is_moving = False
        self.stuck = None
        self.targeted_to_steal = False
        self.stolen = False
        self.always_on_top = False

        # Dealing with hazzards far from screen
        self.stay_within_screen = False
        self.screen_limited = False
        self.offscreen_limit = 100

        # Timeframe attributes
        self.lifetime = 0
        self.max_lifetime = 0  # Keep at 0 or lower to remaing living forever
        self.tick = 0

        ### ---// MOVEMENT ATTRIBUTES //
        # Velocity settings
        self.max_velocity = 10
        self.velocity_x = 0
        self.velocity_y = 0

        # Dynamic area movement settings
        self.area_movement = False
        self.destined_point = None
        self.destined_position = (0, 0)
        self.destined_velocity = 2

        # Following settings
        self.min_magnitude = 0
        self.max_magnitude = 100
        self.follow_strength = 4

        # Push physics settings
        self.push_velocity = (0, 0)
        self.push_weight = 1
        self.push_force = 15
        self.push_tick = 0
        self.push_interval = 5
        self.push_stops_movement = True

        ### ---// VISUAL ATTRIBUTES //
        # Sprite blinking settings
        self.can_blink = False
        self.blink = False
        self.blink_interval = 15

        ### ---// DEBUG ATTRIBUTES //
        self.print_death = False

    # Handles multiple base functions in one to set the object
    def spawn(self, position=(0, 0), velocity=(0, 0), owner=None):
        self.reset()

        if len(position) >= 4:
            self.spawnpoint = (position[2], position[3])
        else:
            self.spawnpoint = position

        self.set_owner(owner)
        self.set_position(position)
        self.set_velocity(velocity)

    # Resets the base values from the object
    def reset(self):
        self.owner = None
        self.spawner = None

        self.alive = True
        self.visible = True
        self.can_collide = True
        self.can_touch = True
        self.can_move = True
        self.is_moving = False

        self.spawnpoint = (0, 0)
        self.set_velocity(0, 0)
        self.push_velocity = (0, 0)
        self.destined_position = (0, 0)
        self.destined_point = None
        self.tick = 0
        self.lifetime = 0
        self.set_size(self.base_size)

    def kill(self):
        self.alive = False
        if self.print_death:
            print(f'Killed {self.name} {self.type} '
                  f'[ID: {self.id}, Position: {self.rect.center}, Lifetime: {self.lifetime}]')

    def set_owner(self, owner):
        self.owner = owner

        if owner:
            self.color = owner.color
        if not self.spawner:
            self.spawner = owner

    # Sets the X and Y velocity vectors for the object.
    # Allows tuple, lists or both values separately as arguments.
    def set_velocity(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            self.velocity_x = min(max(args[0][0], -self.max_velocity), self.max_velocity)
            self.velocity_y = min(max(args[0][1], -self.max_velocity), self.max_velocity)
        elif len(args) == 2:
            self.velocity_x = min(max(args[0], -self.max_velocity), self.max_velocity)
            self.velocity_y = min(max(args[1], -self.max_velocity), self.max_velocity)

    def set_max_velocity(self, max_velocity):
        self.max_velocity = max_velocity

    # Sets the current position vectors for the object at given X and Y coordinates.
    # Allows tuple, lists, separate values and boolean for setting the rect center at the position.
    def set_position(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.rect.x = args[0][0]
            self.rect.y = args[0][1]
        elif len(args) == 2 and isinstance(args[0], (tuple, list)) and args[1] == True:
            self.rect.center = args[0]
        elif len(args) == 2:
            self.rect.x = args[0]
            self.rect.y = args[1]
        elif len(args) == 3 and args[2] == True:
            self.rect.centerx = args[0]
            self.rect.centery = args[1]
        else:
            raise ValueError(
                f'Invalid vectors given: {args}. Possible arguments are:\n'
                f'"x, y" ; (x, y) ; "x, y, centered = True/False" ; (x, y) , centered = True/False')

    # Sets the current size of the object at given X and Y proportions.
    # Allows tuple, lists, separate values and boolean for setting it as the base size.
    def set_size(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.size = tuple(args[0])
        elif len(args) == 2 and isinstance(args[0], (tuple, list)) and args[1] == True:
            self.base_size = tuple(args[0])
            self.size = self.base_size
        elif len(args) == 2:
            self.size = (args[0], args[1])
        elif len(args) == 3 and args[2] == True:
            self.base_size = (args[0], args[1])
            self.size = self.base_size
        else:
            raise ValueError(
                f'Invalid proportions given: {args}. Possible arguments are:\n'
                f'x, y ; (x, y) ; x, y, set_base = True/False ; (x, y), set_base = True/False')

        # Resizes the sprite in the same position
        self.sprite = pg.transform.scale(self.sprite, self.size)
        self.rect = pg.Rect(self.rect.topleft, self.size)

    # Changes or resets the color of the object, including alpha values.
    def set_color(self, custom=None, custom_sprite=None):
        if custom:
            new_color = custom
        else:
            new_color = self.color

        width, height = self.sprite.get_size()
        r, g, b = new_color[:3]
        color_alpha = new_color[3] if len(new_color) > 3 else 255

        # Setting each pixel of the image manually, properly avoiding transparent backgrounds.
        # Locking the image might help performance, but not sure if it helps.
        if custom_sprite:
            sprite = custom_sprite
        else:
            sprite = self.sprite

        sprite.lock()

        for x in range(width):
            for y in range(height):
                current_pixel = sprite.get_at((x, y))
                if current_pixel.a > 0:
                    sprite.set_at((x, y), (r, g, b, color_alpha))

        sprite.unlock()

    def set_destination(self, *args):
        self.area_movement = True
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.destined_position = args[0]
        elif len(args) == 2:
            self.destined_position = (args[0], args[1])
        else:
            raise ValueError(
                f'Invalid coordinates given: {args}. Possible arguments are:\n'
                f'"x, y" ; (x, y)')

    def set_blink(self, can_blink=None, blink_interval=15):
        if can_blink is None:
            can_blink = not self.can_blink

        self.can_blink = can_blink
        self.blink_interval = blink_interval

    # Sets the sprite to a new image, allowing for copying or direct reference
    def set_sprite(self, new_sprite, copy=True):
        self.sprite = new_sprite.copy() if copy else new_sprite
        self.set_size(self.size)

    # Resets the sprite back to the original configuration image
    def reset_sprite(self):
        self.sprite = self.config.get('image', self.NIL_IMAGE).copy()
        self.set_size(self.size)

    # Function for following any given rect, checks if velocity should be kept
    def follow(self, rect, strength=None):
        # Gets the distance threshold from the object to the rect
        direction_x = rect.centerx - self.rect.centerx
        direction_y = rect.centery - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Checks if the distance threshold is valid
        check_distance = self.max_magnitude > magnitude > self.min_magnitude

        if not strength:
            strength = self.follow_strength

        if check_distance:
            new_x = (direction_x / magnitude) * strength
            new_y = (direction_y / magnitude) * strength
            new_x, new_y = round(new_x, 1), round(new_y, 1)

            self.set_velocity(new_x, new_y)
        else:
            self.set_velocity(0, 0)
            self.area_movement = False

    # Initializes pushing object depending on object given
    def push(self, other_object):
        if self.push_tick < self.push_interval:
            return False
        else:
            self.push_tick = 0

        push_force = 15
        if not hasattr(other_object, 'rect') and not isinstance(other_object, pg.Rect):
            raise ValueError(f'Invalid object given: {other_object}. '
                             f'Must be a Rect or class with "rect" attribute')
        elif hasattr(other_object, 'rect'):
            rect = other_object.rect
            if hasattr(other_object, 'push_force'):
                push_force = other_object.push_force
        else:
            rect = other_object

        # Calculating the relative position with both vectors
        relative_collision = self.rect.clip(rect).center
        offset_vector = pg.math.Vector2(self.rect.center) - pg.math.Vector2(relative_collision)

        # This function just normalizes the vector values in unit (-1 to 1)
        if offset_vector.length() != 0:
            offset_vector.normalize_ip()
        force_x = (offset_vector.x * push_force) / self.push_weight
        force_y = (offset_vector.y * push_force) / self.push_weight

        # Add pushing values
        self.push_velocity = (force_x, force_y)
        return True
    
    def update(self, game):
        self.tick += 1

        velocity_x, velocity_y = self.velocity_x, self.velocity_y
        if velocity_x == 0 == velocity_y:
            self.is_moving = False
        else:
            self.is_moving = True

        # Setting the velocity to the target position of any
        if self.area_movement:
            # Creating a rect point goal and centering it to the position the object will move to
            self.destined_point = pg.Rect(0, 0, 10, 10)
            self.destined_point.center = self.destined_position
            self.max_magnitude = 2000
            self.min_magnitude = 10
            self.follow(self.destined_point, self.destined_velocity)

        # System for exponential pushing, ignored if push_velocity never changes
        if self.can_push:
            self.push_tick += 1
        if self.push_velocity != (0, 0):
            self.push_velocity = (self.push_velocity[0] * 0.9, self.push_velocity[1] * 0.9)

            if self.push_stops_movement:
                velocity_x, velocity_y = self.push_velocity[0], self.push_velocity[1]
            else:
                velocity_x += self.push_velocity[0]
                velocity_y += self.push_velocity[1]

            # Check if both X and Y push velocity values are low enough
            if abs(self.push_velocity[0]) < 0.1 > abs(self.push_velocity[1]):
                self.push_velocity = (0, 0)

        if self.can_move:
            self.rect.x += velocity_x
            self.rect.y += velocity_y

        if self.stay_within_screen:
            # Making sure the object stays on screen
            self.rect.clamp_ip(game.screen_limit)
        
        if game.tick % game.FPS == 0:
            self.lifetime += 1

        if 0 < self.max_lifetime < self.lifetime:
            self.kill()

        if self.can_blink and self.tick % self.blink_interval == 0:
            self.blink = not self.blink
        
        if self.screen_limited and self.is_offscreen(game):
            self.kill()

    def is_offscreen(self, game):
        screen_witdh = game.screen.get_width()
        screen_height = game.screen.get_height()

        return (self.rect.right < 0 - self.offscreen_limit or
                self.rect.left > screen_witdh + self.offscreen_limit or
                self.rect.bottom < 0 - self.offscreen_limit or
                self.rect.top > screen_height + self.offscreen_limit)
        
    def draw(self, game):
        if self.visible and not self.blink:
            game.screen.blit(self.sprite, self.rect)

        if game.debug and self.destined_point:
            pg.draw.rect(game.screen, (255, 255, 0), self.destined_point)
