"""
star.py

Defines the Star class for background effects.
"""

import pygame
import random
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Star:
    """
    Represents a star in the background.
    """

    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 1.5)
        self.color = (255, 255, 255)

    def update(self):
        """
        Update the star's position.
        """
        self.x -= self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)

    def draw(self, screen):
        """
        Draw the star on the screen.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
