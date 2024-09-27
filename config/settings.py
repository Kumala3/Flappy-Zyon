"""
settings.py

Contains configuration constants for the game.
"""

import pygame

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCI_FI_BLUE = (0, 200, 255)
SCI_FI_GREEN = (0, 255, 100)

# Game variables
OBSTACLE_GAP = 200
OBSTACLE_WIDTH = 80
OBSTACLE_VELOCITY = -5

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 40)
FONT_SMALL = pygame.font.SysFont("Arial", 24)

# Frame rate
FPS = 60
