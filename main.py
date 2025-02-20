"""
Main module for the components.
This module handles the initialization of the components loop and the rendering process.
"""
import pygame as pg
import traceback
import sys

from western_raid import Game

DEBUG = True

if __name__ == '__main__':
    pg.init()
    game = Game()

    try:
        # Running the game
        game.run()
    except Exception as e:
        print(f"Error while trying to run WESTERN-RAID: {e}")
        if DEBUG: traceback.print_exc()
    finally:
        game.save_data()
        pg.quit()
        sys.exit()