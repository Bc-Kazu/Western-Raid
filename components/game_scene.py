"""
SceneObject class is made to serve other classes that identify as scenes for display,
it holds basic functions for scenery processing specified for Western Raid
"""
import math
from copy import deepcopy

class GameScene:
    # Directory that should contain every process with a corresponding state key
    BASE_STATE_DICT = {}

    def __init__(self, name, screen):
        self.name = name
        self.state = None
        self.screen = screen
        self.state_dict = deepcopy(self.BASE_STATE_DICT)

        self.initialize = False
        self.finalize = False
        self.tick = 0

        self.tween_finished = True
        self.goal_offset = [0, 0]
        self.ui_offset = [0, 0]
        self.tween_velocity = 0

    def start_tween(self, new_offset=None, velocity=50):
        if new_offset is None: new_offset = [0, 0]
        self.goal_offset = new_offset[:]
        self.tween_finished = False
        self.tween_velocity = velocity

    def finish_tween(self):
        self.ui_offset = self.goal_offset[:]
        self.tween_finished = True
        self.tween_velocity = 0

    def tween_interface(self):
        # Gets the distance threshold from the object to the rect
        direction_x = self.goal_offset[0] - self.ui_offset[0]
        direction_y = self.goal_offset[1] - self.ui_offset[1]
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if self.tween_velocity > 1:
            self.tween_velocity *= 0.9
        else:
            self.tween_velocity = 1

        if magnitude > self.tween_velocity:
            self.ui_offset[0] += (direction_x / magnitude) * self.tween_velocity
            self.ui_offset[1] += (direction_y / magnitude) * self.tween_velocity
        else:
            self.finish_tween()

    def set_player_pos(self, game):
        game.player_menu_pos = game.base_menu_pos[:]
        game.player_menu_pos[0] += self.ui_offset[0]
        game.player_menu_pos[1] += self.ui_offset[1]

    def set_offset(self, offset):
        self.ui_offset = offset

    def reset(self):
        self.state = None

        for state in self.state_dict.keys():
            self.reset_state(state)

    def set_state(self, name=None):
        if name:
            if name in self.state_dict:
                self.state = self.state_dict[name]
            else:
                print(f'{name} state for {self.name} scene not found.')
        else:
            self.state = None

    def reset_state(self, name):
        self.state_dict[name] = deepcopy(self.BASE_STATE_DICT[name])

    def _state_check(self, name):
        if self.state and not self.state['finalize']:
            if self.state['name'] == name:
                return True