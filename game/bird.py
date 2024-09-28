"""
bird.py

Defines the Bird class representing the player's character.
"""

import pygame
import os
import sys


class Bird:
    """
    Represents the player's bird (phoenix icon).
    """

    def __init__(self, gravity, flap_strength):
        self.x = 100
        self.y = pygame.display.get_surface().get_height() // 2
        self.velocity = 0
        self.width = 40
        self.height = 40
        self.gravity = gravity
        self.flap_strength = flap_strength
        self.shield = False
        self.shield_timer = 0
        self.image = self.load_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def load_image(self):
        """
        Loads the phoenix image from the assets directory.
        """
        try:
            image_path = os.path.join("assets", "images", "phoenix.png")
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error as e:
            print(f"Unable to load image '{image_path}': {e}")
            pygame.quit()
            sys.exit()

    def update(self):
        """
        Updates the bird's position based on gravity.
        """
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.centery = self.y

    def flap(self):
        """
        Makes the bird flap (move upwards).
        """
        self.velocity = self.flap_strength

    def draw(self, screen):
        """
        Draws the bird on the screen.
        """
        screen.blit(self.image, self.rect)
        if self.shield:
            # Draw shield indicator around bird
            pygame.draw.circle(
                screen, (0, 255, 255), self.rect.center, self.width // 2 + 5, 2
            )
