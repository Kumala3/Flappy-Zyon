"""
helpers.py

Contains helper functions for event handling, game updates, and drawing.
"""

import pygame
import sys
import random
from game.particle import Particle
from game.powerup import PowerUp
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, SCI_FI_GREEN, SCI_FI_BLUE, WHITE, FONT, FONT_SMALL
from game.obstacle import Obstacle

def handle_events(bird, game_state, background_images):
    for event in pygame.event.get():
        # Existing event handling...
        if event.type == pygame.KEYDOWN:
            if game_state['state'] == 'start':
                if event.key == pygame.K_1:
                    game_state['theme'] = 'space'
                    game_state['current_background'] = background_images['space']
                    game_state['state'] = 'level_select'
                elif event.key == pygame.K_2:
                    game_state['theme'] = 'nebula'
                    game_state['current_background'] = background_images['nebula']
                    game_state['state'] = 'level_select'
                elif event.key == pygame.K_3:
                    game_state['theme'] = 'planet'
                    game_state['current_background'] = background_images['planet']
                    game_state['state'] = 'level_select'
            elif game_state['state'] == 'level_select':
                # Level selection code...
                if event.key == pygame.K_e:
                    # Set level to easy
                    game_state['level'] = 'easy'
                    game_state['gravity'] = 0.4
                    game_state['flap_strength'] = -10
                    game_state['state'] = 'playing'
                    bird.gravity = game_state['gravity']
                    bird.flap_strength = game_state['flap_strength']
                elif event.key == pygame.K_m:
                    # Medium level
                    game_state['gravity'] = 0.5
                    game_state['flap_strength'] = -5
                    game_state['state'] = 'playing'
                    bird.gravity = game_state['gravity']
                    bird.flap_strength = game_state['flap_strength']
                elif event.key == pygame.K_h:
                    # Hard level
                    game_state["gravity"] = 0.6
                    game_state["flap_strength"] = 0
                    game_state["state"] = "playing"
                    bird.gravity = game_state["gravity"]
                    bird.flap_strength = game_state["flap_strength"]
        # Rest of the event handling...

def update_game(
    bird,
    obstacles,
    stars,
    game_state,
    particles,
    powerups,
    score_sound,
    game_over_sound,
):
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
        # Existing code...

        # Generate power-ups randomly
        if random.randint(0, 500) == 1:
            powerups.append(PowerUp(SCREEN_WIDTH))

        # Update power-ups
        for powerup in powerups:
            powerup.update()
            if powerup.collide(bird):
                # Handle power-up effect
                if powerup.type == "shield":
                    # Implement shield effect
                    pass
                elif powerup.type == "score_boost":
                    # Implement score boost effect
                    pass
                powerups.remove(powerup)

        # Remove off-screen power-ups
        powerups[:] = [pu for pu in powerups if pu.x + pu.width > 0]

        # Existing collision detection and score update...

    game_state["frame_count"] += 1

def draw_game(screen, bird, obstacles, stars, game_state, particles, powerups):
    # Draw background
    if game_state["current_background"]:
        screen.blit(game_state["current_background"], (0, 0))
    else:
        screen.fill(BLACK)

    # Draw stars
    for star in stars:
        star.draw(screen)

    if game_state["state"] == "playing":
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
        # Draw score
        # Existing code...
