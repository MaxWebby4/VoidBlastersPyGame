import pygame
import random

# Define screen dimensions
screen_width = 800
screen_height = 600

# Power-Up Classes
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

# Health Power-Up (Adds 1 life)
class HealthPowerUp(PowerUp):
    def __init__(self, image):
        super().__init__(image)

    def apply(self, player):
        if player.lives < 5:  # Max lives capped at 5
            player.lives += 1

# Speed Power-Up (Doubles player speed for 10 seconds)
class SpeedPowerUp(PowerUp):
    def __init__(self, image):
        super().__init__(image)

    def apply(self, player):
        player.speed *= 2  # Double speed
        player.speed_powerup_time = pygame.time.get_ticks()  # Track time for 10 seconds

# Double Points Power-Up (Double points for 10 seconds)
class DoublePointsPowerUp(PowerUp):
    def __init__(self, image):
        super().__init__(image)

    def apply(self, game_state):
        game_state.double_points_active = True
        game_state.double_points_time = pygame.time.get_ticks()  # Track time for 10 seconds
