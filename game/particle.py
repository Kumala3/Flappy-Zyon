"""
particle.py

Defines the Particle class for visual effects.
"""

import pygame
import random


class Particle:
    """
    Represents a particle for visual effects.
    """

    def __init__(self, position):
        self.x, self.y = position
        self.radius = random.randint(2, 4)
        self.color = (255, 255, 255)
        self.life = 20  # Frames to live
        self.velocity = [random.uniform(-1, 1), random.uniform(-2, 0)]

    def update(self):
        """
        Update the particle's position and life.
        """
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= 1

    def draw(self, screen):
        """
        Draw the particle on the screen.
        """
        if self.life > 0:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), self.radius
            )
