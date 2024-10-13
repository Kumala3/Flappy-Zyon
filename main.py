"""
main.py

Entry point of the game. Initializes and runs the game loop.
"""

import pygame
import sys
import os
import random
from config.settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from game.bird import Bird
from game.obstacle import Obstacle
from game.star import Star
from game.powerup import PowerUp
from game.particle import Particle
from utils.helpers import handle_events, update_game, draw_game
from utils.high_score import load_high_score, save_high_score


def main():
    """
    Main function to run the game.
    """
    # Initialize Pygame modules
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer module for sounds

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sci-Fi Flappy Bird")

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Load sounds
    flap_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "flap.mp3"))
    score_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "score.mp3"))
    game_over_sound = pygame.mixer.Sound(
        os.path.join("assets", "sounds", "game_over.mp3")
    )

    # Load background images
    background_images = {
        "space": pygame.image.load(
            os.path.join("assets", "images", "bg-space.png")
        ).convert(),
        "nebula": pygame.image.load(
            os.path.join("assets", "images", "bg-nebula.png")
        ).convert(),
        "planet": pygame.image.load(
            os.path.join("assets", "images", "bg-planet.png")
        ).convert(),
    }

    # Initialize game variables
    default_gravity = 0.5
    default_flap_strength = -10

    # Load high score
    high_score = load_high_score()

    # Game state dictionary
    game_state = {
        "state": "start",
        "score": 0,
        "high_score": high_score,
        "frame_count": 0,
        "reset": False,
        "level": None,
        "gravity": default_gravity,
        "flap_strength": default_flap_strength,
        "theme": None,
        "current_background": None,
        "score_saved": False,
    }

    # Initialize game objects
    bird = Bird(game_state["gravity"], game_state["flap_strength"])
    obstacles = []
    stars = [Star() for _ in range(50)]
    particles = []
    powerups = []

    # Main game loop
    running = True
    while running:
        clock.tick(FPS)

        # Update frame count
        game_state["frame_count"] += 1

        # Handle events
        handle_events(bird, game_state, background_images)

        # Update game objects and state
        if game_state["reset"]:
            # Reset the game
            bird = Bird(game_state["gravity"], game_state["flap_strength"])
            obstacles = []
            stars = [Star() for _ in range(50)]
            particles = []
            powerups = []
            game_state["score"] = 0
            game_state["frame_count"] = 0
            game_state["state"] = "start"
            game_state["reset"] = False
            game_state["level"] = None
            game_state["theme"] = None
            game_state["current_background"] = None
            game_state["score_saved"] = False
        else:
            update_game(
                bird,
                obstacles,
                stars,
                game_state,
                particles,
                powerups,
                score_sound,
                game_over_sound,
                FPS,
            )

        # Save high score if game over
        if game_state["state"] == "game_over" and not game_state.get(
            "score_saved", False
        ):
            if game_state["score"] > game_state["high_score"]:
                game_state["high_score"] = game_state["score"]
                save_high_score(game_state["high_score"])
            game_state["score_saved"] = True

        # Draw everything
        draw_game(screen, bird, obstacles, stars, game_state, particles, powerups)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
