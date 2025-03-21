import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Set the frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (34, 177, 76)  # Green field
RED = (255, 0, 0)  # Red player color

# Fonts for text display
font = pygame.font.SysFont(None, 55)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Player's size
        self.image.fill(RED)  # Color of the player (Red)
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Starting position
        self.rect.y = SCREEN_HEIGHT - 100

        self.velocity = 0
        self.speed = 5
        self.jump_power = -15
        self.on_ground = False

    def update(self):
        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Handle jumping
        if self.on_ground and keys[pygame.K_SPACE]:
            self.velocity = self.jump_power
            self.on_ground = False

        # Gravity
        self.velocity += 1  # Apply gravity
        self.rect.y += self.velocity

        # Prevent the player from going below the screen
        if self.rect.y >= SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
            self.velocity = 0
            self.on_ground = True

    def handle_collisions(self, platforms):
        """Handle collisions with platforms to prevent the player from going through them"""
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Player falling down (colliding with the top of the platform)
                if self.velocity > 0 and self.rect.bottom <= platform.rect.top + self.velocity:
                    self.rect.bottom = platform.rect.top
                    self.velocity = 0
                    self.on_ground = True
                # Player jumping up (colliding with the bottom of the platform)
                elif self.velocity < 0 and self.rect.top >= platform.rect.bottom + self.velocity:
                    self.rect.top = platform.rect.bottom
                    self.velocity = 0  # Stop upward velocity
                    break  # Stop checking after the first upward collision

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)  # Color of the platform (field/ground)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Initialize the surface and set a transparent background
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)  # Make the surface transparent

        # Draw the flagpole (black rectangle)
        self.pole_width = 10
        self.pole_height = 80
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.pole_width, self.pole_height))  # Black pole

        # Draw the triangle (half the height of the pole)
        triangle_height = self.pole_height // 2  # Half the height of the pole
        pygame.draw.polygon(self.image, (255, 0, 0), [
            (self.pole_width, 0),  # Top of the pole (right side)
            (self.pole_width + self.pole_height, triangle_height),  # Bottom right of the triangle
            (self.pole_width, triangle_height)  # Bottom left of the triangle
        ])

        # Set the rectangle for positioning the flag
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.pole_height  # Position the flag to stand on the platform

def main():
    player = Player()

    # Create a group for sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create platform(s)
    platforms = pygame.sprite.Group()

    # Add multiple platforms at different heights and positions
    platform1 = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)  # Ground platform
    platform2 = Platform(100, SCREEN_HEIGHT - 150, 200, 20)  # Second platform
    platform3 = Platform(300, SCREEN_HEIGHT - 250, 200, 20)  # Third platform
    platform4 = Platform(500, SCREEN_HEIGHT - 350, 200, 20)  # Fourth platform

    platforms.add(platform1, platform2, platform3, platform4)  # Add to platform group
    all_sprites.add(platform1, platform2, platform3, platform4)  # Add to all sprites group

    # Create flag at the end of the level, positioned on the platform
    flag = Flag(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50)  # Flag position
    all_sprites.add(flag)

    # Create a group for the flag
    flags = pygame.sprite.Group()
    flags.add(flag)

    # Run the game loop
    level_completed = False
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update player and check collisions
        player.update()
        player.handle_collisions(platforms)

        # Collision with the flag (level completion)
        if pygame.sprite.spritecollide(player, flags, False):
            level_completed = True

        # Fill the screen with blue (sky)
        screen.fill(BLUE)

        # Draw all sprites
        all_sprites.draw(screen)

        # Display level completion message if level is completed
        if level_completed:
            # Display "Level Completed" message
            text = font.render("Level Completed!", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        # Update the screen
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
