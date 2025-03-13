"""
SceneObject class is made to serve other classes that identify as scenes for display,
it holds basic functions for scenery processing specified for Western Raid
"""
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