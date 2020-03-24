import pygame
import random
import math
from pygame import mixer

# Intialize the pygame needed for code to work
pygame.init()

# Creates screen width and height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("stars.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

running = True

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("space-invaders.png")
player_x = 370
player_y = 490
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy_ufo.png"))
    enemy_x.append(random.randint(0, 800))
    enemy_y.append(random.randint(50, 100))
    enemy_x_change.append(3.5)
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
# Enemy x direction to the left
score_counter_xl = 0
# Enemy x direction to the right
score_counter_xr = 0
font = pygame.font.Font("freesansbold.ttf", 24)

text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    final_score = over_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(final_score, (270, 300))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Distance between two points
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

x = 0
# Game loop
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background image
    rel_x = x % background.get_rect().width
    screen.blit(background, (rel_x - background.get_rect().width , 0))
    if rel_x < 800:
        screen.blit(background , (rel_x , 0))
    x -=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Bullet sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.set_volume(0.2)
                    bullet_sound.play()
                    # Gets the x coordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player doesn't go out of boundary
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemy_y[i] >= 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            player_x = 370
            break
        # Enemy movement
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 3.5
            # Every 10th level the speed increases by 2
            if score_counter_xr == 10 and score_counter_xr != 0:
                enemy_x_change[i] = enemy_x_change[i] + random.randint(1,3)
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -3.5
            # Every 10th level the speed increases by 2
            if score_counter_xl % 10 == 0 and score_counter_xl != 0:
                enemy_x_change[i] = enemy_x_change[i] - random.randrange(1,3)
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.set_volume(0.2)
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            score_counter_xl += 1
            score_counter_xr += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 100)
        enemy(enemy_x[i], enemy_y[i], i)
    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
