import pygame
import sys
from endless_mode import endless_mode
from level_1 import level_1
from level_2 import level_2
from level_3 import level_3

# Initialize pygame
pygame.init()

# Initialize the mixer for music
pygame.mixer.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load and play background music, looping indefinitely
pygame.mixer.music.load('MainMenuMusic.mp3')
pygame.mixer.music.play(-1)  # The -1 parameter makes it loop indefinitely

# Load the sound effect for button clicks
click_sound = pygame.mixer.Sound('select.wav')

# Adjust volume of sound effects
click_sound.set_volume(0.25)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Define fonts
title_font = pygame.font.Font(None, 100)  # Large font for the title
button_font = pygame.font.Font(None, 54)  # Smaller font for buttons
slider_font = pygame.font.Font(None, 36)  # Smaller font for the slider

# Load a background image
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.clicked = False
        self.hover_scale = 1.0

    def draw(self, screen, mouse_pos):
        is_hovering = self.rect.collidepoint(mouse_pos)

        # Smooth hover animation
        target_scale = 1.1 if is_hovering else 1.0
        self.hover_scale += (target_scale - self.hover_scale) * 0.1

        # Scale the button
        scaled_rect = self.rect.inflate(
            int((self.hover_scale - 1) * self.rect.width),
            int((self.hover_scale - 1) * self.rect.height)
        )

        # Draw button
        pygame.draw.rect(screen, self.hover_color if is_hovering else self.color, scaled_rect, border_radius=20)

        # Draw button text
        text_surface = button_font.render(self.text, True, BLACK)
        screen.blit(text_surface, (
            scaled_rect.x + (scaled_rect.width - text_surface.get_width()) // 2,
            scaled_rect.y + (scaled_rect.height - text_surface.get_height()) // 2
        ))

    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            if not self.clicked:  # Register click only once
                self.clicked = True
                click_sound.play()  # Play click sound
                return True
        if not mouse_click:
            self.clicked = False  # Reset click state when mouse is released
        return False

# Slider class for volume control
class Slider:
    def __init__(self, x, y, width, height, min_val=0.0, max_val=1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = max_val  # Initial slider value (full volume)
        self.handle_rect = pygame.Rect(x + width - 20, y, 20, height)
        self.dragging = False

    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, GRAY, self.rect)
        # Draw handle
        pygame.draw.rect(screen, WHITE, self.handle_rect)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(mouse_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if self.dragging:
            # Move the handle horizontally within the slider bounds
            self.handle_rect.x = max(self.rect.x, min(mouse_pos[0], self.rect.right - self.handle_rect.width))
            # Update the slider value based on the handle's position
            self.value = (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)
            pygame.mixer.music.set_volume(self.value)

# Buttons for the main menu
button_width = 350
button_height = 100
button_spacing = 50  # Space between the buttons
total_width = 2 * button_width + button_spacing
start_x = (screen_width - total_width) // 2

endless_button = Button("ENDLESS MODE", start_x, 300, button_width, button_height, GRAY, WHITE)
campaign_button = Button("MAIN CAMPAIGN", start_x + button_width + button_spacing, 300, button_width, button_height, GRAY, WHITE)

# Add a Settings button at the bottom right
settings_button = Button("SETTINGS", screen_width - 230, screen_height - 60, 200, 40, GRAY, WHITE)

# Buttons for levels (Level 1 to Level 3 for example)
level_buttons = [
    Button("LEVEL 1", 250, 180, 300, 100, GRAY, WHITE),
    Button("LEVEL 2", 250, 330, 300, 100, GRAY, WHITE),
    Button("LEVEL 3", 250, 480, 300, 100, GRAY, WHITE)
]

# Back button at the bottom left of the screen
back_button = Button("BACK", 50, screen_height - 100, 150, 50, GRAY, WHITE)

# Settings screen components
volume_slider = Slider(screen_width // 2 - 150, screen_height // 2 - 50, 300, 20)
exit_game_button = Button("EXIT GAME?", screen_width // 2 - 125, screen_height // 2 + 50, 250, 50, GRAY, WHITE)

# Draw title
def draw_title(screen, text):
    title_surface = title_font.render(text, True, WHITE)
    title_x = (screen_width - title_surface.get_width()) // 2
    title_y = 100
    screen.blit(title_surface, (title_x, title_y))

# Main loop with state management
def game_loop():
    current_screen = "main_menu"  # Keeps track of the current screen
    running = True
    mouse_released = False  # Track if the mouse button has been released

    while running:
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Handle slider events for volume control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif current_screen == "settings":
                volume_slider.handle_event(event)

        # Main Menu Screen
        if current_screen == "main_menu":
            screen.blit(background, (0, 0))
            draw_title(screen, "VOID BLASTERS")
            endless_button.draw(screen, mouse_pos)
            campaign_button.draw(screen, mouse_pos)
            settings_button.draw(screen, mouse_pos)  # Draw the settings button

            if endless_button.is_clicked(mouse_pos, mouse_click):
                print("Endless Mode Selected")
                endless_mode(screen)
            elif campaign_button.is_clicked(mouse_pos, mouse_click):
                print("Main Campaign Selected")
                current_screen = "levels_menu"  # Switch to levels menu

                # Ensure we only proceed after the mouse button is released
                mouse_released = False
            elif settings_button.is_clicked(mouse_pos, mouse_click):
                print("Settings Selected")
                current_screen = "settings"  # Switch to settings screen

        # Levels Menu Screen
        elif current_screen == "levels_menu":
            screen.blit(background, (0, 0))
            # Wait until the mouse is released before processing any new clicks
            if not mouse_click:
                mouse_released = True

            if mouse_released:  # Only process clicks if the mouse has been released
                draw_title(screen, "SELECT LEVEL")
                for i, button in enumerate(level_buttons):
                    button.draw(screen, mouse_pos)
                    if button.is_clicked(mouse_pos, mouse_click):
                        if i == 0:
                            print(f"Level 1 Selected")
                            level_1(screen)
                        elif i == 1:
                            print(f"Level 2 Selected")
                            level_2(screen)
                        elif i == 2:
                            print(f"Level 3 Selected")
                            level_3(screen)

                # Draw the back button and return to main menu if clicked
                back_button.draw(screen, mouse_pos)
                if back_button.is_clicked(mouse_pos, mouse_click):
                    print("Back to Main Menu")
                    current_screen = "main_menu"  # Switch back to the main menu

        # Settings Screen
        elif current_screen == "settings":
            screen.blit(background, (0, 0))
            draw_title(screen, "SETTINGS")
            # Draw "Volume" text above the slider
            volume_text_surface = slider_font.render("Volume", True, WHITE)
            volume_text_x = (screen_width - volume_text_surface.get_width()) // 2
            volume_text_y = screen_height // 2 - 100
            screen.blit(volume_text_surface, (volume_text_x, volume_text_y))
    
            # Draw slider and buttons
            volume_slider.draw(screen)
            exit_game_button.draw(screen, mouse_pos)

            back_button.draw(screen, mouse_pos)
            if back_button.is_clicked(mouse_pos, mouse_click):
                print("Back to Main Menu from Settings")
                current_screen = "main_menu"

            # Exit the game if the "EXIT GAME?" button is clicked
            if exit_game_button.is_clicked(mouse_pos, mouse_click):
                print("Exiting game...Thanks for Playing!")
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Helper function to draw titles
def draw_title(screen, text):
    title_surface = title_font.render(text, True, WHITE)
    title_x = (screen_width - title_surface.get_width()) // 2
    title_y = 100
    screen.blit(title_surface, (title_x, title_y))

if __name__ == "__main__":
    game_loop()
