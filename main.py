import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sci-Fi Flappy Bird")

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCI_FI_BLUE = (0, 200, 255)
SCI_FI_GREEN = (0, 255, 100)

# Fonts
FONT = pygame.font.SysFont("Arial", 40)
FONT_SMALL = pygame.font.SysFont("Arial", 24)

# Game variables
OBSTACLE_GAP = 200
OBSTACLE_WIDTH = 80
OBSTACLE_VELOCITY = -5


class Bird:
    """
    Class representing the player's bird (phoenix icon).
    """

    def __init__(self, gravity, flap_strength):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 40
        self.height = 40
        self.gravity = gravity
        self.flap_strength = flap_strength
        # Load the phoenix image
        self.image = self.load_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def load_image(self):
        """
        Load the phoenix image from an external file.
        """
        try:
            image = pygame.image.load("assets/phoenix.png").convert_alpha()
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error as e:
            print(f"Unable to load image 'phoenix.png': {e}")
            pygame.quit()
            sys.exit()

    def update(self):
        """
        Update the bird's position based on gravity.
        """
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.centery = self.y

    def flap(self):
        """
        Make the bird flap (move upwards).
        """
        self.velocity = self.flap_strength

    def draw(self, screen):
        """
        Draw the bird on the screen.
        """
        screen.blit(self.image, self.rect)


class Obstacle:
    """
    Class representing an obstacle (pair of top and bottom pipes).
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
        Update the obstacle's position.
        """
        self.x += OBSTACLE_VELOCITY

    def draw(self, screen):
        """
        Draw the obstacle on the screen.
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
        Check for collision with the bird.
        """
        bird_rect = bird.rect
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(
            self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y
        )
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


class Star:
    """
    Class representing a star in the background.
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
        self.x += -self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)

    def draw(self, screen):
        """
        Draw the star on the screen.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


def handle_events(bird, game_state):
    """
    Handle user input events.
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
    Update the game objects and game state.
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
    Draw all game objects and UI elements on the screen.
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


def main():
    """
    Main function to run the game.
    """
    # Default gravity and flap_strength
    default_gravity = 0.5
    default_flap_strength = -10

    # Game variables
    bird = Bird(default_gravity, default_flap_strength)
    obstacles = []
    stars = [Star() for _ in range(50)]  # Add stars for sci-fi effect
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
