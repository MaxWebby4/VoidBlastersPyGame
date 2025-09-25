import pygame
import sys
import random
from power_up import HealthPowerUp, SpeedPowerUp, DoublePointsPowerUp

# Initialize pygame clock
clock = pygame.time.Clock()
FPS = 60  # Frames per second

# Initialize the mixer for sound effects
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define screen dimensions
screen_width = 800
screen_height = 600

# Load sound effects
level_win_sound = pygame.mixer.Sound('level_win.wav')
shoot_sound = pygame.mixer.Sound('shoot.mp3')
destroy_asteroid_sound = pygame.mixer.Sound('asteroid_destroy.mp3')
player_damaged_sound = pygame.mixer.Sound('player_damage.mp3')
power_up_sound = pygame.mixer.Sound('power_up.mp3')

# Adjust volume of sound effects
shoot_sound.set_volume(0.25)
destroy_asteroid_sound.set_volume(0.05)
player_damaged_sound.set_volume(0.25)
power_up_sound.set_volume(0.25)

# Load the images
bullet_image = pygame.image.load('bullet.png')
player_ship_image = pygame.image.load('player_ship.png')
asteroid_image = pygame.image.load('enemy_asteroid.png')
explosion_image = pygame.image.load('explosion.png')

# Load power-up images
health_powerup_image = pygame.image.load('health_powerup.png')
speed_powerup_image = pygame.image.load('speed_powerup.png')
double_points_powerup_image = pygame.image.load('double_points_powerup.png')

# Load and resize the background image to fit the screen
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_ship_image
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.base_speed = 5  # Base speed of the player
        self.speed = self.base_speed  # Player's current speed (affected by power-ups)
        self.lives = 3  # Player starts with 3 lives
        self.speed_powerup_time = 0  # Time tracking for speed power-up

    def reset(self):
        """Reset player lives and position."""
        self.lives = 3
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = self.base_speed  # Reset speed to base speed when resetting

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        # Check if speed power-up has expired
        if pygame.time.get_ticks() - self.speed_powerup_time > 10000:  # 10 seconds
            self.speed = self.base_speed  # Reset to base speed after power-up ends

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()  # Play shooting sound

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image  # Use the loaded bullet image
        self.image = pygame.transform.scale(self.image, (10, 40))  # Resize if necessary
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(explosion_image, (60, 60))  # Adjust size if needed
        self.rect = self.image.get_rect(center=(x, y))
        self.start_time = pygame.time.get_ticks()
        self.duration = 200  # Duration of the explosion in milliseconds

    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()

# Game state class for handling power-up effects
class GameState:
    def __init__(self):
        self.double_points_active = False
        self.double_points_time = 0

    def update(self):
        # Disable double points if 10 seconds have passed
        if pygame.time.get_ticks() - self.double_points_time > 10000:
            self.double_points_active = False

# Create groups for sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Level 1 function
def level_1(screen):
    score = 0
    running = True
    score_font = pygame.font.Font(None, 36)
    lives_font = pygame.font.Font(None, 36)
    target_score = 20  # Define the target score for this level
    game_state = GameState()  # Initialize game state for power-ups

    # Reset player lives and position
    player.reset()

    # Clear all enemies and bullets from previous game
    enemies.empty()
    bullets.empty()
    power_ups.empty()
    
    # Also remove enemy sprites from all_sprites
    for sprite in all_sprites:
        if isinstance(sprite, Enemy):
            all_sprites.remove(sprite)

    last_powerup_spawn = pygame.time.get_ticks()  # Initialize power-up spawn timer
    powerup_respawn_timer = 10000  # Power-up spawns every 10 seconds

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Spawn enemies
        if random.random() < 0.02:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Power-up spawning logic
        now = pygame.time.get_ticks()
        if now - last_powerup_spawn > powerup_respawn_timer:
            power_up_type = random.choice([HealthPowerUp, SpeedPowerUp, DoublePointsPowerUp])
            if power_up_type == HealthPowerUp:
                power_up = HealthPowerUp(health_powerup_image)
            elif power_up_type == SpeedPowerUp:
                power_up = SpeedPowerUp(speed_powerup_image)
            else:
                power_up = DoublePointsPowerUp(double_points_powerup_image)

            power_ups.add(power_up)
            all_sprites.add(power_up)

            last_powerup_spawn = now  # Reset power-up spawn timer

        # Update player, enemies, bullets, and power-ups
        player.update(keys)
        enemies.update()
        bullets.update()
        power_ups.update()
        explosions.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            explosions.add(explosion)
            all_sprites.add(explosion)
            if game_state.double_points_active:
                score += 2  # Double points for kills
            else:
                score += 1
            destroy_asteroid_sound.play()
        
        # Check for enemy-player collisions
        player_hits = pygame.sprite.spritecollide(player, enemies, True)
        if player_hits:
            player.lives -= 1  # Lose a life when hit by an enemy
            player_damaged_sound.play()
            if player.lives <= 0:
                # Clear all enemies and bullets before restarting
                enemies.empty()
                bullets.empty()
                all_sprites.empty()
                all_sprites.add(player)
                running = False  # End the game when lives are 0

        # Check for player collisions with power-ups
        power_up_hits = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_hits:
            if isinstance(power_up, SpeedPowerUp):
                player.speed = player.base_speed * 2  # Double the player's speed
                player.speed_powerup_time = pygame.time.get_ticks()  # Start power-up timer
            else:
                power_up.apply(player if isinstance(power_up, HealthPowerUp) else game_state)

            power_up_sound.play()

        game_state.update()  # Update game state to handle power-up effects

        # Check if the player has reached the target score
        if score >= target_score:
            level_complete(screen, score)
            running = False

        # Redraw screen
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw lives
        lives_text = lives_font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lives_text, (screen_width - 120, 10))

        pygame.display.flip()

    # Game over logic
    game_over(screen, score)

# Function to display level complete message
def level_complete(screen, score):
    level_complete_font = pygame.font.Font(None, 100)
    screen.fill(BLACK)

    # Play the level win sound
    level_win_sound.play()

    # Display "Level Complete"
    level_complete_text = level_complete_font.render("Level Complete", True, WHITE)
    screen.blit(level_complete_text, (screen_width // 2 - level_complete_text.get_width() // 2, screen_height // 2 - level_complete_text.get_height() // 2 - 50))

    # Display the player's score
    score_font = pygame.font.Font(None, 50)
    score_text = score_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 20))

    pygame.display.flip()
    pygame.time.wait(3000)  # Pause for 3 seconds before closing

# Game over screen
def game_over(screen, score):
    game_over_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 50)
    screen.fill(BLACK)

    # Display "Game Over"
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2 - 50))

    # Display the player's score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 20))

    pygame.display.flip()
    pygame.time.wait(3000)  # Pause for 3 seconds before closing
