import pygame
import random

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH = 500
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 255, 0)
RED = (255, 0, 0)

# Load images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')

# Set up game elements    
player_pos = [WIDTH // 2, HEIGHT - 50]
player_speed = 5
player_health = 3
enemies = []
enemy_speed = 2
enemy_spawn_rate = 5
enemy_health = 2
bullets = []
bullet_speed = 7

# Set up game fonts
font = pygame.font.SysFont(None, 30)

# Define functions
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def spawn_enemy():
    enemy_pos = [random.randint(5, WIDTH - enemy_img.get_width()), 5]
    enemies.append(enemy_pos)

def move_enemies():
    global player_health
    for enemy_pos in enemies:
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > HEIGHT:
            enemies.remove(enemy_pos)
            player_health -= 1

def shoot():
    bullet_pos = [player_pos[0] + player_img.get_width() // 2 - bullet_img.get_width() // 2, player_pos[1]]
    bullets.append(bullet_pos)

def move_bullets():
    for bullet_pos in bullets:
        bullet_pos[1] -= bullet_speed
        if bullet_pos[1] < 0:
            bullets.remove(bullet_pos)

def collision_detection():
    global score
    for enemy_pos in enemies:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_img.get_width(), enemy_img.get_height())
        for bullet_pos in bullets:
            bullet_rect = pygame.Rect(bullet_pos[0], bullet_pos[1], bullet_img.get_width(), bullet_img.get_height())
            if enemy_rect.colliderect(bullet_rect):
                enemies.remove(enemy_pos)
                bullets.remove(bullet_pos)
                score += 10

def game_over():
    global running
    if player_health <= 0:
        running = False

# Start game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    elif keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_img.get_width():
        player_pos[0] += player_speed
    elif keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    elif keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_img.get_height():
        player_pos[1] += player_speed

    # Handle enemy spawning
    if random.randint(1, 100) <= enemy_spawn_rate:
        spawn_enemy()

    # Move game elements
    move_enemies()
    move_bullets()

    # Handle collision detection
    collision_detection()

    # Handle game over
    game_over()

    # Draw game elements
    window.fill(WHITE)
    for enemy_pos in enemies:
        window.blit(enemy_img, enemy_pos)
    for bullet_pos in bullets:
        window.blit(bullet_img, bullet_pos)
    window.blit(player_img, player_pos)
    draw_text(f"Score: {score}", font, BLACK, WIDTH - 70, 10)
    draw_text(f"Health: {player_health}", font, RED, WIDTH // 2, 10)

    pygame.display.update()
    clock.tick(60) 
