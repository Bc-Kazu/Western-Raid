from random import randint, choice, choices
from config import LEVEL_CONFIG, POWER_UPS, ITEMS, BRICKS
from assets import LEVELS_ENVIROMENT, PICKUPS_CONFIG

from components.objects.terrain import Terrain
from components.objects.pickup import PickUp
from utils.chance import weight_choices

class Level:
    def __init__(self, index, config, game):
        config = LEVEL_CONFIG[config]
        self.index = index
        self.color = (255, 255, 255)

        # Getting values from configuration dictionary
        self.spawn_types = config['spawn_types']
        self.background_color = config['background']
        self.terrain_noise = config['terrain_noise']
        self.terrain_area_reduction = config['terrain_area_reduction']

        self.round_time = config['round_time']
        self.ambush_time = randint(self.round_time - 120, self.round_time - 100)
        self.difficulty_time = config['difficulty_time']

        self.max_bandits = config['max_bandits']
        self.bandit_spawnrate = config['bandit_spawnrate']
        self.bandit_spawn_multi = config['bandit_spawn_multi']
        self.max_spawn_count = config['max_spawn_count']
        self.spawn_start_time = config['spawn_start_time']
        self.max_increase_time = 50

        # Setting map and base values
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

        # Default style settings
        self.ufo = game.ufo
        self.ufo_pos = (game.screen_width // 2, game.screen_height // 2 - 30)
        self.ufo.set_position(self.ufo_pos, True)
        self.ufo.spawn_blocks()

        # Breakout style settings
        """self.ufo_pos = (game.screen_width // 2, game.screen_height // 6)
        game.ufo.set_position(self.ufo_pos, True)

        breakout_size = ((game.screen_width - 220) // len(BREAKOUT_SHAPE[0]), 16)
        game.ufo.spawn_blocks(BREAKOUT_SHAPE, BREAKOUT_COLORS, breakout_size)"""

        # Tower style settings
        # game.ufo.spawn_blocks(TOWER_SHAPE, TOWER_COLORS)

        self.map = self.create_map(game)

        for terrain in self.map:
            terrain.draw(game)
            terrain.set_decoration()

        for terrain in self.map:
            terrain.distance_check(self)

        for terrain in self.map:
            if not terrain.alive:
                self.map.remove(terrain)

        game.state = 'round'
        game.sound.play('sandwreck', -1)


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

    def spawn_bandit(self, game):
        # Determine spawn settings
        spawn_multiplier = self.bandit_spawn_multi[1] if self.ambush_mode else self.bandit_spawn_multi[0]
        number_spawned = randint(1, self.max_spawn_count + game.player_count * self.ambush_mode)
        max_bandits = self.max_bandits + (spawn_multiplier * game.player_count)
        bandit_spawnrate = max(1, self.bandit_spawnrate - (15 * game.player_count))  # Prevent division by zero

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
                chances = [bandit[1] + (bandit[3] if self.ambush_mode else 0) for bandit in spawns]

                chosen_bandit = choices(population=spawns, weights=chances)[0]
                bandit = game.bandit_pool_dict[chosen_bandit[0]].get()
                bandit.spawn(start_pos, None, self)
                self.bandits.append(bandit)

    # Base function for updating all instances in a list
    def update_instance(self, game, instance_list):
        for instance in instance_list:
            if instance.alive:
                instance.update(game)

                if instance.type == 'bullet':
                    self.ufo.collide_check(game, instance)
                if instance.type == 'enemy' and instance.active:
                    self.bandit_count += 1
            else:
                instance_list.remove(instance)

    # Main function to run the gameplay logic and physics.
    def run(self, game):
        # Clearing the map depending on certain conditions
        if self.defeat or game.victory_transition[0]:
            self.bandits = []
            self.bullets = []
            self.objects = []
            self.ufo.set_regenerate(False)
            self.can_spawn_bandits = False

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
        self.update_instance(game, self.map)
        self.update_instance(game, self.objects)
        self.update_instance(game, self.gadgets)
        self.update_instance(game, self.bandits)
        self.update_instance(game, self.bullets)