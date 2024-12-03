import pygame
import sys
import os
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 100, 255)

# Paths to games
GAMES = {
    "TETRIS": "yt.teteris/main.py",  # Ensure this path is correct
    "ECHOES OF THE FORGOTTEN": "Echos of The Forgotten/game.py",  # Ensure correct path
    "CONNECT 4": "./Connect_Four.py",  # Updated path
    "SPACE SHOOTER": "Space Shooter/Space Shooter.py",  # Update this to correct path
}

# Fonts
TITLE_FONT = pygame.font.Font(None, 70)
BUTTON_FONT = pygame.font.Font(None, 50)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arcade Odyssey")


def run_game(game_path):
    """Run the selected game."""
    absolute_path = os.path.abspath(game_path)
    game_dir = os.path.dirname(absolute_path)
    if os.path.exists(absolute_path):
        try:
            print(f"Launching {absolute_path} from {game_dir}")  # Debug print
            subprocess.run(["python3", absolute_path], cwd=game_dir, check=True)
        except Exception as e:
            print(f"Error running game: {e}")
    else:
        print(f"Error: {absolute_path} not found!")


def render_button(text, x, y, width, height, mouse_pos, clicked, action=None):
    """Render a button and execute its action if clicked."""
    button_color = HOVER_COLOR if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height else GRAY
    pygame.draw.rect(screen, button_color, (x, y, width, height))

    text_surface = BUTTON_FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    # Trigger the action only on a single click
    if clicked and x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        return action
    return None


def main_menu():
    print("Starting the main menu...")  # Debug print
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting the main menu...")  # Debug print
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                clicked = True

        # Render title
        title_surface = TITLE_FONT.render("Arcade Odyssey", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Render buttons for each game
        start_y = 200
        button_width = 550
        button_height = 70
        button_gap = 20

        for i, (game_name, game_path) in enumerate(GAMES.items()):
            action = render_button(
                game_name,
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + i * (button_height + button_gap),
                button_width,
                button_height,
                mouse_pos,
                clicked,
                action=lambda path=game_path: run_game(path),
            )
            if action:
                print(f"Running {game_name}...")  # Debug print
                action()

        # Render Exit button
        exit_action = render_button(
            "EXIT",
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + len(GAMES) * (button_height + button_gap) + 40,
            button_width,
            button_height,
            mouse_pos,
            clicked,
            action=lambda: sys.exit(),
        )
        if exit_action:
            print("Exiting the program...")  # Debug print
            exit_action()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    print("Launching Arcade Odyssey...")  # Debug print
    main_menu()