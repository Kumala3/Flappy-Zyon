"""
helpers.py

Contains helper functions for event handling, game updates, and drawing.
"""

import pygame
import sys
import random
from game.particle import Particle
from game.powerup import PowerUp
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    SCI_FI_GREEN,
    SCI_FI_BLUE,
    WHITE,
    FONT,
    FONT_SMALL,
)
from game.obstacle import Obstacle


def handle_events(bird, game_state, background_images, flap_sound):
    """
    Handles user input events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state["state"] == "start":
                if event.key == pygame.K_1:
                    game_state["theme"] = "space"
                    game_state["current_background"] = background_images["space"]
                    game_state["state"] = "level_select"
                elif event.key == pygame.K_2:
                    game_state["theme"] = "nebula"
                    game_state["current_background"] = background_images["nebula"]
                    game_state["state"] = "level_select"
                elif event.key == pygame.K_3:
                    game_state["theme"] = "planet"
                    game_state["current_background"] = background_images["planet"]
                    game_state["state"] = "level_select"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif game_state["state"] == "level_select":
                if event.key == pygame.K_e:
                    # Set level to easy
                    game_state["level"] = "easy"
                    game_state["gravity"] = 0.4
                    game_state["flap_strength"] = -10
                    game_state["state"] = "playing"
                    game_state["start_time"] = pygame.time.get_ticks()
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
                elif event.key == pygame.K_m:
                    # Medium level
                    game_state["level"] = "medium"
                    game_state["gravity"] = 0.5
                    game_state["flap_strength"] = -9
                    game_state["state"] = "playing"
                    game_state["start_time"] = pygame.time.get_ticks()
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
                elif event.key == pygame.K_h:
                    # Hard level
                    game_state["level"] = "hard"
                    game_state["gravity"] = 0.6
                    game_state["flap_strength"] = -8
                    game_state["state"] = "playing"
                    game_state["start_time"] = pygame.time.get_ticks()
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif game_state["state"] == "playing":
                if event.key == pygame.K_SPACE:
                    bird.flap()
                    flap_sound.play()
                elif event.key == pygame.K_g:
                    # Enable shield cheat
                    bird.shield = True
                    bird.shield_timer = 300  # Shield lasts for 300 frames (5 seconds)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif game_state["state"] == "game_over":
                if event.key == pygame.K_r:
                    # Reset the game
                    game_state["reset"] = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                game_state["start_tme"] = pygame.time.get_ticks()


def update_game(
    bird,
    obstacles,
    stars,
    game_state,
    particles,
    powerups,
    score_sound,
    game_over_sound,
    FPS,
):
    """
    Updates the game objects and game state.
    """
    # Update stars
    for star in stars:
        star.update()

    if game_state["state"] == "playing":
        # Update bird
        bird.update()

        # Generate particles
        particles.append(Particle((bird.x, bird.y)))

        # Update particles
        particles[:] = [p for p in particles if p.life > 0]
        for particle in particles:
            particle.update()

        # Update obstacles
        if game_state["frame_count"] % 90 == 0:
            obstacles.append(Obstacle(SCREEN_WIDTH))
        for obstacle in obstacles:
            obstacle.update()

        # Remove obstacles that have gone off screen
        obstacles[:] = [o for o in obstacles if o.x + o.width > 0]

        # Generate power-ups every 4 seconds
        if game_state["frame_count"] % (4 * FPS) == 0:
            powerups.append(PowerUp(SCREEN_WIDTH))

        # Update power-ups
        for powerup in powerups:
            powerup.update()
            if powerup.collide(bird):
                # Handle power-up effect
                if powerup.type == "shield":
                    # Implement shield effect
                    bird.shield = True
                    bird.shield_timer = 300  # Shield lasts for 300 frames
                elif powerup.type == "score_boost":
                    # Implement score boost effect
                    game_state["score"] += 5
                powerups.remove(powerup)

        # Remove off-screen power-ups
        powerups[:] = [pu for pu in powerups if pu.x + pu.width > 0]

        # Check for collisions
        collision = False
        for obstacle in obstacles:
            if obstacle.collide(bird):
                if hasattr(bird, "shield") and bird.shield:
                    # Bird is shielded, ignore collision
                    continue
                else:
                    collision = True
                    break

        if collision:
            game_over_sound.play()
            game_state["state"] = "game_over"

        # Update score
        for obstacle in obstacles:
            if obstacle.x + obstacle.width < bird.x and not obstacle.passed:
                obstacle.passed = True
                game_state["score"] += 1
                score_sound.play()

        # Check if bird hits the ground or goes off the screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            game_over_sound.play()
            game_state["state"] = "game_over"

        # Update shield timer
        if hasattr(bird, "shield") and bird.shield:
            bird.shield_timer -= 1
            if bird.shield_timer <= 0:
                bird.shield = False


def draw_game(screen, bird, obstacles, stars, game_state, particles, powerups):
    """
    Draws all game objects and UI elements on the screen.
    """
    # Draw background
    if game_state["current_background"]:
        screen.blit(game_state["current_background"], (0, 0))
    else:
        screen.fill(BLACK)

    # Draw stars
    for star in stars:
        star.draw(screen)

    if game_state["state"] == "start":
        # Draw start screen
        title_text = FONT.render("Sci-Fi Flappy Bird", True, SCI_FI_GREEN)
        theme_text = FONT_SMALL.render(
            "Press 1 for Space, 2 for Nebula, 3 for Planet", True, SCI_FI_BLUE
        )
        quit_text = FONT_SMALL.render("Press Q to Quit", True, SCI_FI_GREEN)
        screen.blit(
            title_text,
            (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3),
        )
        screen.blit(
            theme_text,
            (SCREEN_WIDTH // 2 - theme_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        screen.blit(
            quit_text,
            (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30),
        )
    elif game_state["state"] == "level_select":
        # Draw level selection screen
        title_text = FONT.render("Select Difficulty", True, SCI_FI_GREEN)
        instruction_text = FONT_SMALL.render(
            "Press E for Easy, M for Medium, H for Hard", True, SCI_FI_BLUE
        )
        quit_text = FONT_SMALL.render("Press Q to Quit", True, SCI_FI_GREEN)
        screen.blit(
            title_text,
            (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3),
        )
        screen.blit(
            instruction_text,
            (
                SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                SCREEN_HEIGHT // 2,
            ),
        )
        screen.blit(
            quit_text,
            (
                SCREEN_WIDTH // 2 - quit_text.get_width() // 2,
                SCREEN_HEIGHT // 2 + 30,
            ),
        )
    elif game_state["state"] == "playing":
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        # Draw power-ups
        for powerup in powerups:
            powerup.draw(screen)
        # Draw bird
        bird.draw(screen)
        # Draw particles
        for particle in particles:
            particle.draw(screen)

        # Ensure start time isn't None
        if game_state["start_time"] is None:
            game_state["start_time"] = pygame.time.get_ticks()

        # Calculate elapsed time
        current_time = pygame.time.get_ticks()
        elapsed_time_ms = current_time - game_state["start_time"]
        elapsed_time_sec = elapsed_time_ms // 1000  # Convert to seconds

        # Format the time as MM:SS
        hours, remainder = divmod(elapsed_time_sec, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_display = f"Time: {int(hours):02}:{int(minutes):02}:{int(seconds):02}"

        time_text = FONT_SMALL.render(time_display, True, WHITE)

        # Draw time played
        text_rect = time_text.get_rect()
        text_rect.topright = (
            SCREEN_WIDTH - 10,
            10,
        )  # 10 pixels from the top-right corner
        screen.blit(time_text, text_rect)

        # Draw score
        score_text = FONT.render(str(game_state["score"]), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

        # Check if shield is active
        if hasattr(bird, "shield") and bird.shield:
            shield_seconds_left = bird.shield_timer // 60
            shield_seconds_left_text = FONT_SMALL.render(
                f"Shield active for {shield_seconds_left:02} s", True, SCI_FI_GREEN
            )
            screen.blit(shield_seconds_left_text, (10, 10))
    elif game_state["state"] == "game_over":
        # Draw game over screen
        game_over_text = FONT.render("Game Over", True, SCI_FI_GREEN)
        score_text = FONT.render(
            "Score: " + str(game_state["score"]), True, SCI_FI_BLUE
        )
        high_score_text = FONT_SMALL.render(
            "Highest Score: " + str(game_state["high_score"]), True, WHITE
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
            high_score_text,
            (
                SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
                SCREEN_HEIGHT // 2 + 40,
            ),
        )
        screen.blit(
            retry_text,
            (
                SCREEN_WIDTH // 2 - retry_text.get_width() // 2,
                SCREEN_HEIGHT // 2 + 80,
            ),
        )

    pygame.display.flip()
