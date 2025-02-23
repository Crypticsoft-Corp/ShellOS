import pygame
import subprocess
import os
import json
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1017, 660
FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT = 1920, 1080
TASKBAR_HEIGHT = 30
ICON_PATH = "SYSTEM/Graphical_Shell/icons/shellos.png"
BG_IMAGE_PATH = "SYSTEM/Graphical_Shell/wallpaper.png"
LAUNCHER_ICON_PATH = "SYSTEM/Graphical_Shell/icons/launcher.ico"
SETTINGS_FILE = "time_settings.json"

# Set up the display with resizable flag
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ShellOS 3.0")
icon = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon)

# Load images
bg_image = pygame.image.load(BG_IMAGE_PATH)
launcher_icon = pygame.image.load(LAUNCHER_ICON_PATH)

# Colors
TASKBAR_COLOR = (37, 37, 37)  # #252525
LAUNCHER_BG_COLOR = (50, 0, 85)  # #320055
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont(None, 24)
clock_font = pygame.font.SysFont(None, 24)

# Create button rectangle and clock label
launcher_button_rect = pygame.Rect(5, 2, 26, 26)  # Adjusted for icon size
version_label_rect = pygame.Rect(WIDTH - 250, HEIGHT - 25, 240, 20)

# Scale launcher icon to fit inside button while maintaining aspect ratio
launcher_icon_scaled = pygame.transform.smoothscale(launcher_icon, (22, 22))

# Initial variables
running = True
clock = pygame.time.Clock()
fullscreen = False
current_width, current_height = WIDTH, HEIGHT

# Function to open launcher
def open_launcher():
    launcher_script = os.path.join(os.getcwd(), 'SYSTEM', 'Graphical_Shell', 'Launcher.py')
    subprocess.Popen(['python', launcher_script])

# Function to toggle fullscreen
def toggle_fullscreen():
    global fullscreen, current_width, current_height
    fullscreen = not fullscreen
    if fullscreen:
        current_width, current_height = FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        current_width, current_height = WIDTH, HEIGHT
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    resize_window(current_width, current_height)

# Function to load saved time settings
def load_time_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            saved_date = settings.get("date", "2000-01-01")
            saved_time = settings.get("time", "00:00:00")
            return saved_date, saved_time
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

# Function to get current time based on settings
def get_current_time():
    saved_date, saved_time = load_time_settings()
    if saved_date and saved_time:
        try:
            formatted_datetime = datetime.strptime(f"{saved_date} {saved_time}", "%Y-%m-%d %H:%M:%S")
            return formatted_datetime.strftime("%H:%M %B %d, %Y")
        except ValueError:
            pass  # If there's an error, fallback to system time
    now = datetime.now()
    return now.strftime("%H:%M %B %d, %Y")

# Function to update elements on resize
def resize_window(new_width, new_height):
    global current_width, current_height, bg_image_scaled
    current_width, current_height = new_width, new_height
    bg_image_scaled = pygame.transform.scale(bg_image, (new_width, new_height - TASKBAR_HEIGHT))

# Initial scaling of background image
resize_window(WIDTH, HEIGHT)

# Main loop
while running:
    # Draw the resized wallpaper first
    screen.blit(bg_image_scaled, (0, TASKBAR_HEIGHT))

    # Draw the taskbar on top to ensure it isn't overridden
    pygame.draw.rect(screen, TASKBAR_COLOR, (0, 0, current_width, TASKBAR_HEIGHT))

    # Draw the launcher button
    pygame.draw.rect(screen, LAUNCHER_BG_COLOR, launcher_button_rect)

    # Center and draw the launcher icon
    icon_x = launcher_button_rect.x + (launcher_button_rect.width - launcher_icon_scaled.get_width()) // 2
    icon_y = launcher_button_rect.y + (launcher_button_rect.height - launcher_icon_scaled.get_height()) // 2
    screen.blit(launcher_icon_scaled, (icon_x, icon_y))

    # Draw the clock, fixed to the right side
    current_time = get_current_time()
    clock_text = clock_font.render(current_time, True, WHITE)
    clock_label_x = current_width - clock_text.get_width() - 10  # Position it near the right edge
    screen.blit(clock_text, (clock_label_x, (TASKBAR_HEIGHT - clock_text.get_height()) // 2))  # Center vertically

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
        elif event.type == pygame.VIDEORESIZE:
            resize_window(event.w, event.h)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if launcher_button_rect.collidepoint(event.pos):
                open_launcher()

    # Force display update to ensure changes take effect
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
