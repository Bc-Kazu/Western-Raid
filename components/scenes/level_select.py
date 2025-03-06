''' ===================================================================== '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN LEVEL SELECT  ========== '''
''' ===================================================================== '''

from assets import TITLE_SPRITE_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, \
    TITLE_SPRITE, UFO_SPRITE, TITLE_SPRITE2, UFO_SPRITE2, \
    TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT, TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2, LEVEL_FRAMES, LEVEL_ICONS, \
    LEVEL_FRAMES_RECT, LEVEL_ICONS_RECT, LEVEL_LOCKS, LEVEL_LOCKS_RECT

from components.game_scene import GameScene
from utils.colors import Colors
colors = Colors()

class LevelSelect(GameScene):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        super().reset()
        self.bobbing_interval = 30

        self.player_offset = [0, -100, 100]
        self.player_bobbing = 15

        self.sprites_dict = {
            1: [[TITLE_SPRITE, TITLE_SPRITE_RECT], [TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT],
                      [UFO_SPRITE, UFO_SPRITE_RECT]],
            2: [[TITLE_SPRITE2, TITLE_SPRITE_RECT2], [TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2],
                      [UFO_SPRITE2, UFO_SPRITE_RECT2]]
        }

    def draw(self, game):
        game.screen.fill(colors.space_blue)
        game.stars.update(game)

        game.text.level_select.draw(game)
        game.text.select_tip.draw(game)

        for i in range(len(LEVEL_FRAMES)):
            getattr(game.text, f"level{i + 1}_select").current_color = colors.grey
            LEVEL_FRAMES[i].set_alpha(100)
            LEVEL_ICONS[i].set_alpha(100)

        # Set active level to highlighted state
        if 1 <= game.base_level <= 3:
            getattr(game.text, f"level{game.base_level}_select").current_color = colors.white
            LEVEL_FRAMES[game.base_level - 1].set_alpha(255)
            LEVEL_ICONS[game.base_level - 1].set_alpha(255)

        for i in range(1, 6):
            getattr(game.text, f"level{i}_select").draw(game)

        # Draw level frames, icons, and locks if locked
        for i in range(len(LEVEL_FRAMES)):
            game.screen.blit(LEVEL_FRAMES[i], LEVEL_FRAMES_RECT[i])
            game.screen.blit(LEVEL_ICONS[i], LEVEL_ICONS_RECT[i])

            if not game.data[f"level{i + 1}"]["unlocked"]:
                game.screen.blit(LEVEL_LOCKS[i], LEVEL_LOCKS_RECT[i])

        # Draw players
        if game.tick % self.bobbing_interval == 0:
            game.player_bobbing = -game.player_bobbing

        for player in [game.player_1, game.player_2]:
            if not player:
                continue

            for sprite in self.sprites_dict[player.id]:
                sprite[1].centerx = game.screen_width // 2 + self.player_offset[player.id]
                sprite[1].centery = game.player_menu_y
                if sprite == self.sprites_dict[player.id][2]:
                    sprite[1].y -= 20

                if player.id % 2 == 0:
                    sprite[1].y -= game.player_bobbing
                else:
                    sprite[1].y += game.player_bobbing

                if sprite == self.sprites_dict[player.id][1]:
                    sprite[1].centerx -= 4

                game.screen.blit(sprite[0], sprite[1])
