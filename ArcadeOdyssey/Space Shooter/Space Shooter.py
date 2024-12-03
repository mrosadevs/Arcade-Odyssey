import random
import pygame
import math
import time
from pygame import mixer

def load_image(path):
    try:
        return pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image '{path}': {e}")
        pygame.quit()
        raise SystemExit(f"Missing or corrupted file: {path}")

def load_sound(path):
    try:
        return mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound '{path}': {e}")
        return None  # Optionally return None if the sound isn't critical

# Initialize Pygame
pygame.init()
mixer.init()

icon = load_image('icon.png')
background = load_image('Space.Background.jpg')
player_img = load_image('spaceship1.png')
bullet_img = load_image('bullet.png')

laser_sound = load_sound('Laser.Shot.mp3')
explosion_sound = load_sound('Ship.Explosion.mp3')

if laser_sound:
    laser_sound.set_volume(0.5)
if explosion_sound:
    explosion_sound.set_volume(0.7)


# Load sound effects
laser_sound = mixer.Sound('Laser.Shot.mp3')
explosion_sound = mixer.Sound('Ship.Explosion.mp3')
laser_sound.set_volume(0.5)  # Reduce laser sound volume
explosion_sound.set_volume(0.7)  # Reduce explosion sound volume

# Screen setup
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption('Space Warrior')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

enemy_img = []
enemyX = []
enemyY = []
enemy_SpeedX = []
enemy_SpeedY = []

# Increased the number of enemies
no_of_enemies = 10

# Initialize enemy attributes
for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load('Enemyship.png'))
    enemyX.append(random.randint(0, 900 - 64))  # Adjust for enemy width
    enemyY.append(random.randint(30, 150))     # Random Y position for variety
    enemy_SpeedX.append(0.5)
    enemy_SpeedY.append(30)

# Background and player setup
background = pygame.image.load('Space.Background.jpg')
player_img = pygame.image.load('spaceship1.png')
bullet_img = pygame.image.load('bullet.png')
bullet_state = "ready"  # Indicates if the bullet is ready to fire

# Initial player position and movement variables
playerX = 400
playerY = 560
changeX = 0

# Score and font setup
score = 0
font = pygame.font.SysFont('Arial', 32, True)

def score_text():
    img = font.render(f'Score: {score}', True, 'white')
    screen.blit(img, (10, 10))

font_gameover = pygame.font.SysFont('Arial', 50, True)

def gameover_text():
    img_gameover = font_gameover.render('GAME OVER', True, 'white')
    screen.blit(img_gameover, (300, 250))

# Bullet position and speed
bulletX = 0
bulletY = playerY
bullet_speedY = -4

# Firing rate control variables
bullet_time = time.time()  # Store the current time when the player can fire again
bullet_delay = 0.1  # Time interval between bullets in seconds (lower = faster)

# Functions to draw objects
def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet_img, (x + 16, y + 10))  # Center the bullet relative to the player
    laser_sound.play()  # Play laser shot sound

def is_collision(bulletX, bulletY, enemyX, enemyY):
    distance_squared = (bulletX - enemyX) ** 2 + (bulletY - enemyY) ** 2
    return distance_squared < 27 ** 2  # Use squared threshold

# Main game loop
running = True
game_over = False  # Variable to track if the game is over

while running:
    # Draw background
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:  # Allow movement and firing only if the game is not over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    changeX = -1  # Adjust speed
                if event.key == pygame.K_RIGHT:
                    changeX = 1
                if event.key == pygame.K_SPACE:
                    current_time = time.time()
                    if bullet_state == "ready" and current_time - bullet_time > bullet_delay:
                        bulletX = playerX  # Set bullet's starting position to the player's current position
                        fire_bullet(bulletX, bulletY)
                        bullet_time = current_time  # Update the last time a bullet was fired

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    changeX = 0

    if not game_over:
        # Update player position
        playerX += changeX

        # Enemy movement and logic for each enemy
        for i in range(no_of_enemies):
            enemyX[i] += enemy_SpeedX[i]
            if enemyX[i] <= 0 or enemyX[i] >= 900 - enemy_img[i].get_width():
                enemy_SpeedX[i] *= -1
                enemyY[i] += enemy_SpeedY[i]

            # Check for collision with bullet
            if is_collision(bulletX, bulletY, enemyX[i], enemyY[i]):
                bullet_state = "ready"
                enemyX[i] = random.randint(0, 900 - enemy_img[i].get_width())
                enemyY[i] = random.randint(30, 150)
                score += 1
                explosion_sound.play()  # Play explosion sound

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bullet_state == "fired":
            fire_bullet(bulletX, bulletY)
            bulletY += bullet_speedY
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        # Check for Game Over (if any enemy reaches the player)
        for i in range(no_of_enemies):
            if enemyY[i] > playerY - enemy_img[i].get_height():
                game_over = True

        # Keep the player within the screen boundaries
        playerX = max(0, min(playerX, 900 - player_img.get_width()))

        # Draw the player
        player(playerX, playerY)

    else:
        # Display Game Over text
        gameover_text()

    # Always display the score
    score_text()

    # Update the display
    pygame.display.update()
