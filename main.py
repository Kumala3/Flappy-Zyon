import pygame
import sys
import os
from config.settings import *
from game.bird import Bird
from game.obstacle import Obstacle
from game.star import Star
from utils.helpers import handle_events, update_game, draw_game
from utils.high_score import load_high_score, save_high_score


def main():
    """
    Main function to run the game.
    """
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer module for sounds

    # Load sounds
    flap_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "flap.wav"))
    score_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "score.wav"))
    game_over_sound = pygame.mixer.Sound(
        os.path.join("assets", "sounds", "game_over.wav")
    )

    # Rest of the code...
