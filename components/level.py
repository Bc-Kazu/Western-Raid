from random import randint, choice, choices

from components.objects.gadgets.bot_shooter import BotShooter
from components.objects.gadgets.turret_shield import TurretShield
from components.objects.gadgets.turret_shooter import TurretShooter
from configurations.pickup_config import POWER_UPS, ITEMS, BRICKS
from assets import LEVELS_ENVIROMENT, PICKUPS_CONFIG, SMALL_FONT, TEXT_FONT, GADGET_CONFIG
from configurations.level_config import LEVEL_CONFIG

from components.objects.terrain import Terrain
from components.objects.pickup import PickUp
from utils.chance import weight_choices
from utils.text import Text
from utils.colors import Colors
colors = Colors()

class Level:
    def __init__(self, index, config, game):
        config = LEVEL_CONFIG[config]
        self.index = index
        self.color = (255, 255, 255)

        # Getting values from configuration dictionary
        self.spawn_types = config['spawn_types']
        self.background_color = config['background']
        self.music = config['music']
        self.terrain_noise = config['terrain_noise']
        self.terrain_area_reduction = config['terrain_area_reduction']

        self.round_time = config['round_time']
        self.ambush_time = randint(self.round_time - 130, self.round_time - 110)
        self.difficulty_time = config['difficulty_time']

        self.max_bandits = config['max_bandits']
        self.bandit_spawnrate = config['bandit_spawnrate']
        self.bandit_spawn_multi = config['bandit_spawn_multi']
        self.max_spawn_count = config['max_spawn_count']
        self.spawn_start_time = config['spawn_start_time']
        self.max_increase_time = 50

        # Setting map and base values
        self.started = False
        self.ambush_mode = False
        self.victory = False
        self.defeat = False
        self.difficulty_incremented = False
        self.can_spawn_bandits = True
        self.time_elapsed = 0
        self.bandit_count = 0

        # List for modules to render and update within the level
        self.objects = []
        self.gadgets = []
        self.bullets = []
        self.bandits = []
        self.message_popups = []

        # Default style settings
        self.ufo = game.ufo
        self.base_ufo_pos = (game.screen_width // 2, game.screen_height // 2 - 30)
        self.ufo.set_position(self.base_ufo_pos[0], -self.ufo.size[1], True)
        self.ufo.spawn_blocks(game)

        # Breakout style settings
        """self.ufo_pos = (game.screen_width // 2, game.screen_height // 6)
        game.ufo.set_position(self.ufo_pos, True)

        breakout_size = ((game.screen_width - 220) // len(BREAKOUT_SHAPE[0]), 16)
        game.ufo.spawn_blocks(game, BREAKOUT_SHAPE, BREAKOUT_COLORS, breakout_size)"""

        # Tower style settings
        # game.ufo.spawn_blocks(game, TOWER_SHAPE, TOWER_COLORS)

        self.map = self.create_map(game)

        for terrain in self.map:
            terrain.update(game)
            terrain.set_decoration()

        for terrain in self.map:
            terrain.distance_check(self)

        for terrain in self.map:
            if not terrain.alive:
                self.map.remove(terrain)

    def start(self, game):
        self.started = True
        game.sound.play(self.music, -1)


    # This function takes care of drawing the map randomly and automatically.
    def create_map(self, game):
        terrain_list = []
        terrain_amount = 50
        terrain_counter = 1

        for index in range(terrain_amount):
            if randint(0, terrain_amount * self.terrain_noise) >= randint(0, terrain_amount):
                terrain_counter += 1
                # Get a random bandit to spawn depending on chance
                spawns = []
                chances = []

                for terrain_type in LEVELS_ENVIROMENT[f'level{self.index}']:
                    chances.append(terrain_type[0])
                    spawns.append(terrain_type[1])

                random_terrain = choices(population=spawns, weights=chances)[0]

                pos_x = randint(0, game.screen_width)
                pos_y = randint(0, game.screen_height)
                new_asset = Terrain(random_terrain, terrain_counter, self)
                new_asset.set_position(pos_x, pos_y, True)
                new_asset.set_color()
                terrain_list.append(new_asset)

        return terrain_list

    def spawn_pickup(self, pickup_type, position):
        if not pickup_type:
            return

        name = ''

        if pickup_type == 'power_up':
            name = weight_choices(POWER_UPS)
        elif pickup_type == 'item':
            name = weight_choices(ITEMS)
        elif pickup_type == 'brick':
            name = weight_choices(BRICKS)

        new_pickup = PickUp(PICKUPS_CONFIG[name])
        new_pickup.spawn(position, None, self)
        if name == 'bomb':
            new_pickup.set_size((50, 50))
        if name == 'gift_bomb':
            new_pickup.set_size((70, 70))

        self.objects.append(new_pickup)

    def spawn_gadget(self, game, name, player):
        class_list = {'turret_shooter': TurretShooter,
                      'turret_shield': TurretShield,
                      'bot_shooter': BotShooter}

        if name in class_list:
            config = GADGET_CONFIG[name]
            gadget_count = 0
            for gadget in self.gadgets:
                if gadget.name == name:
                    gadget_count += 1

            if gadget_count >= ITEMS[name][2]:
                return False

            new_gadget = class_list[name](config)
            new_gadget.spawn(player.rect.center, (0, 0), player)
            self.gadgets.append(new_gadget)

            player.holding = new_gadget if config['can_hold'] else None
            return True

    def spawn_bandit(self, game):
        # Determine spawn settings
        spawn_multiplier = self.bandit_spawn_multi[1] if self.ambush_mode else self.bandit_spawn_multi[0]
        number_spawned = randint(1, self.max_spawn_count + game.player_count * self.ambush_mode)
        max_bandits = self.max_bandits + (spawn_multiplier * game.player_count)
        bandit_spawnrate = max(1, self.bandit_spawnrate - (15 * game.player_count))

        # Creating bandits
        if game.tick % bandit_spawnrate == 0 and self.bandit_count < max_bandits:
            for _ in range(number_spawned):
                # Spawn position logic
                spawn_direction = choice(['left', 'right'])
                spawn_settings = {
                    'left': (-50, randint(10, game.screen_height - 40), randint(30, 100)),
                    'right': (game.screen_width, randint(10, game.screen_height - 40),
                              game.screen_width - randint(70, 140))}
                x, y, dest_x = spawn_settings[spawn_direction]
                start_pos = [x, y, dest_x, y]

                # Bandit selection logic
                spawns = [bandit for bandit in self.spawn_types
                    if not bandit[2] or (bandit[2] and self.ambush_mode)]

                chances = []
                for bandit in spawns:
                    if bandit[0] == 'robber' and len(self.gadgets) < 1:
                        spawns.remove(bandit)
                        continue
                    chances.append(bandit[1] + (bandit[3] if self.ambush_mode else 0))

                chosen_bandit = choices(population=spawns, weights=chances)[0]
                bandit = game.bandit_pool_dict[chosen_bandit[0]].get()
                bandit.spawn(start_pos, None, self)
                self.bandits.append(bandit)

    def spawn_message(self, style, text, position):
        message = Text(text, position, SMALL_FONT)
        message.preset(style, (0, 0), 120)

        if style == 'popup':
            if text[1].isdigit():
                message.preset('popup', (0, -4), 50)
            elif text[-2:] == 'PU':
                message.set_font(TEXT_FONT)
                message.preset('popup', (0, -5), 80)
                message.set_color_blink(True, 8, colors.light_pink)

        self.message_popups.append(message)

    # Base function for updating all instances in a list
    def update_instance(self, game, instance_list):
        for instance in instance_list:
            if instance.alive:
                instance.update(game)

                if instance.type == 'enemy' and instance.active:
                    self.bandit_count += 1
                if instance.type == 'text' and instance.style == 'popup':
                    instance.set_velocity(
                        instance.velocity_x * 0.9,
                        instance.velocity_y * 0.9,
                    )
            else:
                instance_list.remove(instance)

    # Main function to run the gameplay logic and physics.
    def run(self, game):
        # Clearing the map depending on certain conditions
        if self.defeat or (game.scene.state and game.scene.state['name'] == 'victory'):
            self.bandits = []
            self.bullets = []
            self.ufo.set_regenerate(False)
            self.can_spawn_bandits = False

        if self.started:
            if self.time_elapsed >= self.spawn_start_time and self.can_spawn_bandits:
                self.spawn_bandit(game)

            # Counting every second of the round elapsed
            if game.tick % game.FPS == 0 and not self.defeat:
                self.time_elapsed += 1
                self.difficulty_incremented = False

            # Increasing difficulty every difficulty_time interval
            if (self.time_elapsed != 0 and self.time_elapsed % self.difficulty_time == 0
                    and not self.difficulty_incremented):
                self.difficulty_incremented = True
                self.bandit_spawnrate = max(60, self.bandit_spawnrate - 15)

                # Increasing max bandit count every max_increase_time interval
                if self.time_elapsed % self.max_increase_time == 0:
                    self.max_bandits += 1

            self.bandit_count = 0

        # Updating every game component class
        if not self.defeat:
            if game.player_1:
                game.player_1.update(game)
            if game.player_2:
                game.player_2.update(game)

        self.ufo.update(game)
        self.ufo.collide_check(game)
        self.update_instance(game, self.map)
        self.update_instance(game, self.objects)
        self.update_instance(game, self.gadgets)
        self.update_instance(game, self.bandits)
        self.update_instance(game, self.bullets)
        self.update_instance(game, self.message_popups)

        # Checking for scene conditions
        if not self.ufo.alive and not self.defeat:
            self.defeat = True
            game.scene.set_state('defeat')

        if self.time_elapsed >= self.round_time and not self.victory:
            self.victory = True
            game.scene.set_state('rebuild')

        ambush_allowed = (not self.ambush_mode and not self.victory
                          and not self.defeat and not game.scene.state)
        if self.time_elapsed > self.ambush_time and ambush_allowed:
            self.ambush_mode = True
            game.scene.set_state('ambush')