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
        self.can_spawn_early = config['can_spawn_early']

        # Setting map and base values
        self.ambush_mode = False
        self.victory = False
        self.defeat = False
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
            terrain.distance_check(self)

        for terrain in self.map:
            terrain.set_decoration()

        game.state = 'round'
        game.sound.play('sandwreck', -1)


    ''' This function takes care of drawing the map automatically, but manually making a
        grid in the same size as the game's display. '''
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
        # Creating bandits
        if not self.ambush_mode:
            number_spawned = randint(1, self.max_spawn_count)
            max_bandits = self.max_bandits + (self.bandit_spawn_multi[0] * game.player_count)
        else:
            number_spawned = randint(0, self.max_spawn_count + game.player_count)
            max_bandits = self.max_bandits + (self.bandit_spawn_multi[1] * game.player_count)

        bandit_spawnrate = int(self.bandit_spawnrate - (15 * game.player_count))

        if game.tick % bandit_spawnrate == 0 and self.bandit_count < max_bandits:
            for new_bandit in range(number_spawned):
                spawn_direction = choice(['left', 'right'])
                start_pos = [0, 0,  # Position that spawns at first
                             0, 0]  # Destined spawnpoint

                if spawn_direction == 'left':
                    start_pos[0] = -50
                    start_pos[1] = randint(10, game.screen_height - 40)
                    start_pos[2] = randint(30, 100)
                    start_pos[3] = start_pos[1]
                if spawn_direction == 'right':
                    start_pos[0] = game.screen_width
                    start_pos[1] = randint(10, game.screen_height - 40)
                    start_pos[2] = game.screen_width - randint(70, 140)
                    start_pos[3] = start_pos[1]

                # Get a random bandit to spawn depending on chance
                spawns = []
                chances = []

                for bandit_type in self.spawn_types:
                    if not bandit_type[2]:
                        spawns.append(bandit_type)
                        if not self.ambush_mode:
                            chances.append(bandit_type[1])
                        else:
                            chances.append(bandit_type[1] + bandit_type[3])
                    elif bandit_type[2] and self.ambush_mode:
                        spawns.append(bandit_type)
                        chances.append(bandit_type[1])

                choosen_bandit = choices(population=spawns, weights=chances)[0]
                bandit = game.bandit_pool_dict[choosen_bandit[0]].get()
                bandit.spawn(start_pos, None, self)
                self.bandits.append(bandit)

    def run(self, game):
        if self.defeat or game.victory_transition[0]:
            self.bandits = []
            self.bullets = []
            self.objects = []
            self.can_spawn_early = False
            self.ufo.set_regenerate(False)

        if self.can_spawn_early: self.spawn_bandit(game)
        self.bandit_count = len(self.bandits)

        if game.tick % game.FPS == 0 and not self.defeat:
            self.time_elapsed += 1

        # increasing difficulty every 15 seconds
        if self.time_elapsed % self.difficulty_time == 0:
            self.bandit_spawnrate = max(60, self.bandit_spawnrate - 15)

        for terrain in self.map:
            if terrain.alive:
                terrain.update(game)
            else:
                self.map.remove(terrain)

        # Updating UFO
        if not self.defeat:
            if game.player_1:
                game.player_1.update(game)
            if game.player_2:
                game.player_2.update(game)

        self.ufo.update(game)

        for obj in self.objects:
            if obj.alive:
                obj.update(game)
            else:
                self.objects.remove(obj)

        for gadget in self.gadgets:
            if gadget.alive:
                gadget.update(game)
            else:
                self.objects.remove(gadget)

        # Updating bandits
        for bandit in self.bandits:
            if bandit.alive:
                # Getting a random target
                bandit.get_target(game)

                # Applhying chance to spawn loot on death
                bandit.update(game)
                bandit.collide_check(game)

                bandit.push_check(game, game.player_1)
                bandit.push_check(game, game.player_2)
            else:
                self.bandits.remove(bandit)

        for bullet in self.bullets:
            if bullet.alive and bullet.lifetime <= bullet.max_lifetime:
                bullet.update(game)

                # Collision check with players, shields and UFO
                bullet.collide_check(game, game.player_1)
                bullet.collide_check(game, game.player_2)
                self.ufo.collide_check(game, bullet)
            else:
                self.bullets.remove(bullet)