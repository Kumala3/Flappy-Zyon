"""
powerup.py

Defines the PowerUp class for power-up items.
"""

import pygame
import random
import os
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, OBSTACLE_VELOCITY


class PowerUp:
    """
    Represents a power-up in the game.
    """

    def __init__(self, x):
        self.x = x
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.type = random.choice(["shield", "score_boost"])
        self.width = 30
        self.height = 30
        self.image = self.load_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = OBSTACLE_VELOCITY

    def load_image(self):
        """
        Load the power-up image based on its type.
        """
        try:
            image_path = os.path.join("assets", "images", f"{self.type}.png")
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error as e:
            print(f"Unable to load image '{image_path}': {e}")
            pygame.quit()

    def update(self):
        """
        Update the power-up's position.
        """
        self.x += self.speed
        self.rect.centerx = self.x

    def draw(self, screen):
        """
        Draw the power-up on the screen.
        """
        screen.blit(self.image, self.rect)

    def collide(self, bird):
        """
        Check for collision with the bird.
        """
        return self.rect.colliderect(bird.rect)
