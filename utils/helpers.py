"""
helpers.py

Contains helper functions for event handling, game updates, and drawing.
"""

import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, SCI_FI_GREEN, SCI_FI_BLUE, WHITE, FONT, FONT_SMALL
from game.obstacle import Obstacle


def handle_events(bird, game_state):
    """
    Handles user input events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state["state"] == "playing":
                    bird.flap()
            elif event.key == pygame.K_e:
                if game_state["state"] == "start":
                    # Set level to easy
                    game_state["level"] = "easy"
                    game_state["gravity"] = 0.4
                    game_state["flap_strength"] = -10
                    game_state["state"] = "playing"
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
            elif event.key == pygame.K_m:
                if game_state["state"] == "start":
                    # Set level to medium
                    game_state["level"] = "medium"
                    game_state["gravity"] = 0.5
                    game_state["flap_strength"] = -10
                    game_state["state"] = "playing"
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
            elif event.key == pygame.K_h:
                if game_state["state"] == "start":
                    # Set level to hard
                    game_state["level"] = "hard"
                    game_state["gravity"] = 0.6
                    game_state["flap_strength"] = -9
                    game_state["state"] = "playing"
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
            elif event.key == pygame.K_r:
                if game_state["state"] == "game_over":
                    # Reset the game
                    game_state["reset"] = True
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()


def update_game(bird, obstacles, stars, game_state):
    """
    Updates the game objects and game state.
    """
    # Update stars
    for star in stars:
        star.update()

    if game_state["state"] == "playing":
        # Update bird
        bird.update()

        # Update obstacles
        if game_state["frame_count"] % 90 == 0:
            obstacles.append(Obstacle(SCREEN_WIDTH))
        for obstacle in obstacles:
            obstacle.update()

        # Remove obstacles that have gone off screen
        obstacles[:] = [
            obstacle for obstacle in obstacles if obstacle.x + obstacle.width > 0
        ]

        # Check for collisions
        for obstacle in obstacles:
            if obstacle.collide(bird):
                game_state["state"] = "game_over"

        # Update score
        for obstacle in obstacles:
            if obstacle.x + obstacle.width < bird.x and not obstacle.passed:
                obstacle.passed = True
                game_state["score"] += 1

        # Check if bird hits the ground or goes off the screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            game_state["state"] = "game_over"

        game_state["frame_count"] += 1


def draw_game(screen, bird, obstacles, stars, game_state):
    """
    Draws all game objects and UI elements on the screen.
    """
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        star.draw(screen)

    if game_state["state"] == "start":
        # Draw start screen with level selection
        title_text = FONT.render("Sci-Fi Flappy Bird", True, SCI_FI_GREEN)
        instruction_text = FONT_SMALL.render(
            "Press E for Easy, M for Medium, H for Hard", True, SCI_FI_BLUE
        )
        screen.blit(
            title_text,
            (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3),
        )
        screen.blit(
            instruction_text,
            (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
    elif game_state["state"] == "playing":
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        # Draw bird
        bird.draw(screen)
        # Draw score
        score_text = FONT.render(str(game_state["score"]), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
    elif game_state["state"] == "game_over":
        # Draw game over screen
        game_over_text = FONT.render("Game Over", True, SCI_FI_GREEN)
        score_text = FONT.render(
            "Score: " + str(game_state["score"]), True, SCI_FI_BLUE
        )
        retry_text = FONT_SMALL.render(
            "Press R to Retry or Q to Quit", True, SCI_FI_GREEN
        )
        screen.blit(
            game_over_text,
            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3),
        )
        screen.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        screen.blit(
            retry_text,
            (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50),
        )

    pygame.display.flip()
