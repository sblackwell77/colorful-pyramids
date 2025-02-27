import pygame
import random



# Initialize Pygame
pygame.init()

# Initialize Pygame's mixer (sound) module
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('/Users/sevenblackwell/Downloads/PASTEL GHOST ~ DARK BEACH [ ezmp3.cc ].mp3')  
pygame.mixer.music.play(-1)

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load images
background = pygame.image.load('/Users/sevenblackwell/Downloads/recipe-page-main/space.background.png')  # Your space background image
player_image = pygame.image.load('/Users/sevenblackwell/Downloads/recipe-page-main/spaceship.png')       # Your player spaceship image
enemy_image = pygame.image.load('/Users/sevenblackwell/Downloads/recipe-page-main/enemy.png')       # Your enemy ship image
bullet_image = pygame.image.load('/Users/sevenblackwell/Downloads/recipe-page-main/bullet Small.png')          # Your bullet image

# Scale images (optional)
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (10, 30))

# Player properties
player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 8

# Bullet properties
bullet_speed = 15
bullets = []

# Enemy properties
enemy_speed = 5
enemies = []
enemy_spawn_rate = 25  # Higher = fewer enemies, Lower = more enemies

# Background scrolling
bg_y1 = 0
bg_y2 = -screen_height
bg_scroll_speed = 3

# Colors
white = (255, 255, 255)

# Clock for frame rate control
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("monospace", 35)

# Game loop flag
game_over = False

# Score
score = 0

def draw_background():
    global bg_y1, bg_y2
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))
    bg_y1 += bg_scroll_speed
    bg_y2 += bg_scroll_speed
    if bg_y1 >= screen_height:
        bg_y1 = -screen_height
    if bg_y2 >= screen_height:
        bg_y2 = -screen_height

def draw_player():
    screen.blit(player_image, player_pos)

def fire_bullet(bullet_pos):
    screen.blit(bullet_image, bullet_pos)

def spawn_enemy():
    enemy_pos = [random.randint(0, screen_width - player_size), 0]
    enemies.append(enemy_pos)

def draw_enemy(enemy_pos):
    screen.blit(enemy_image, enemy_pos)

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos
    if (ex < px < ex + player_size or ex < px + player_size < ex + player_size) and \
       (ey < py < ey + player_size or ey < py + player_size < ey + player_size):
        return True
    return False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append([player_pos[0] + player_size // 2 - 5, player_pos[1]])

    # Move bullets
    bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]

    # Spawn enemies
    if random.randint(1, enemy_spawn_rate) == 1:
        spawn_enemy()

    # Move enemies
    enemies = [[e[0], e[1] + enemy_speed] for e in enemies if e[1] < screen_height]

    # Collision detection between player and enemies
    for enemy in enemies:
        if detect_collision(player_pos, enemy):
            game_over = True

    # Collision detection between bullets and enemies
    enemies = [e for e in enemies if not any(b[0] in range(e[0], e[0] + player_size) and b[1] in range(e[1], e[1] + player_size) for b in bullets)]
    bullets = [b for b in bullets if not any(b[0] in range(e[0], e[0] + player_size) and b[1] in range(e[1], e[1] + player_size) for e in enemies)]

    # Clear screen
    screen.fill(white)

    # Draw background
    draw_background()

    # Draw player
    draw_player()

    # Draw bullets
    for bullet in bullets:
        fire_bullet(bullet)

    # Draw enemies
    for enemy in enemies:
        draw_enemy(enemy)

    # Display score
    score += 1
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Refresh display
    pygame.display.update()

    # Frame rate control
    clock.tick(30)

# Quit Pygame
pygame.quit()
