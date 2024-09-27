"""
obstacle.py

Defines the Obstacle class representing obstacles in the game.
"""

import pygame
import random
from config.settings import (
    SCREEN_HEIGHT,
    OBSTACLE_GAP,
    OBSTACLE_WIDTH,
    SCI_FI_BLUE,
    OBSTACLE_VELOCITY,
)


class Obstacle:
    """
    Represents an obstacle (pair of top and bottom pipes).
    """

    def __init__(self, x):
        self.x = x
        self.width = OBSTACLE_WIDTH
        self.gap = OBSTACLE_GAP
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom_y = self.top_height + self.gap
        self.color = SCI_FI_BLUE
        self.passed = (
            False  # Used to check if the bird has passed the obstacle for scoring
        )

    def update(self):
        """
        Updates the obstacle's position.
        """
        self.x += OBSTACLE_VELOCITY

    def draw(self, screen):
        """
        Draws the obstacle on the screen.
        """
        # Draw the top obstacle
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        # Draw the bottom obstacle
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y),
        )

    def collide(self, bird):
        """
        Checks for collision with the bird.
        """
        bird_rect = bird.rect
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(
            self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y
        )
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
