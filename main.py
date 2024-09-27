"""
main.py

Entry point of the game. Initializes and runs the game loop.
"""

import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.bird import Bird
from game.obstacle import Obstacle
from game.star import Star
from utils.helpers import handle_events, update_game, draw_game


def main():
    """
    Main function to run the game.
    """
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sci-Fi Flappy Bird")

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Default gravity and flap_strength
    default_gravity = 0.5
    default_flap_strength = -10

    # Game variables
    bird = Bird(default_gravity, default_flap_strength)
    obstacles = []
    stars = [Star() for _ in range(50)]
    game_state = {
        "state": "start",
        "score": 0,
        "frame_count": 0,
        "reset": False,
        "level": None,
        "gravity": default_gravity,
        "flap_strength": default_flap_strength,
    }

    # Main game loop
    running = True
    while running:
        clock.tick(FPS)

        # Handle events
        handle_events(bird, game_state)

        # Update game objects and state
        if game_state["reset"]:
            # Reset the game
            bird = Bird(game_state["gravity"], game_state["flap_strength"])
            obstacles = []
            stars = [Star() for _ in range(50)]
            game_state["score"] = 0
            game_state["frame_count"] = 0
            game_state["state"] = "start"
            game_state["reset"] = False
            game_state["level"] = None
        else:
            update_game(bird, obstacles, stars, game_state)

        # Draw everything
        draw_game(screen, bird, obstacles, stars, game_state)

    pygame.quit()


if __name__ == "__main__":
    main()
