
import pygame
import random
from enemy import Enemy
from enemy_bullet import EnemyBullet

pygame.init()

# Game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

# -------------------------
# PLAYER SETTINGS
# -------------------------

player = pygame.Rect(375, 530, 50, 30)
player_speed = 8

player_image = pygame.image.load("Space_invaders.character.png")
player_image = pygame.transform.scale(player_image, (50, 30))

# Player bullets
bullets = []
bullet_speed = 8
shoot_delay = 700
last_shot = pygame.time.get_ticks()

# Player lives
lives = 3
last_player_hit = -1000
hit_cooldown = 1000

font = pygame.font.SysFont(None, 36)

# -------------------------
# ENEMY SETTINGS
# -------------------------

alien_images = [
    pygame.image.load("images/alien 1 transparent.png"),
    pygame.image.load("images/alien 2 transparent.png"),
    pygame.image.load("images/alien 3 transparent.png")
]

enemies = []
enemy_bullets = []

# Create 35 enemies
for row in range(5):
    for col in range(7):
        x = 190 + col * 60
        y = 40 + row * 50

        image = alien_images[row % len(alien_images)]

        enemy = Enemy(x, y, image)
        enemies.append(enemy)

# Enemy movement
direction = 1

# Enemy shooting
last_shot_time = pygame.time.get_ticks()
shot_delay = 1200

# -------------------------
# MAIN GAME LOOP
# -------------------------

running = True

while running:

    current_time = pygame.time.get_ticks()

    screen.fill((0, 0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # -------------------------
    # PLAYER SHOOTING
    # -------------------------

    if keys[pygame.K_SPACE] and current_time - last_shot > shoot_delay:

        bullet = pygame.Rect(
            player.centerx - 2,
            player.top,
            5,
            10
        )

        bullets.append(bullet)
        last_shot = current_time

    # Move player bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed

        pygame.draw.rect(screen, (255, 255, 255), bullet)

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # -------------------------
    # PLAYER MOVEMENT
    # -------------------------

    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        player.x = max(player.x, 0)

    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        player.x = min(player.x, 750)

    # Draw player
    screen.blit(player_image, player)

    # -------------------------
    # ENEMY MOVEMENT
    # -------------------------

    for enemy in enemies:
        enemy.move(direction)

    hit_edge = (
        (direction == 1 and any(
            enemy.rect.right >= 800 for enemy in enemies
        ))
        or
        (direction == -1 and any(
            enemy.rect.left <= 0 for enemy in enemies
        ))
    )

    if hit_edge:
        direction *= -1

        for enemy in enemies:
            enemy.y += 20
            enemy.rect.y = enemy.y

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # -------------------------
    # ENEMY SHOOTING
    # -------------------------

    if enemies and current_time - last_shot_time >= shot_delay:

        shooter = random.choice(enemies)

        bullet = EnemyBullet(
            shooter.rect.centerx - 2,
            shooter.rect.bottom
        )

        enemy_bullets.append(bullet)

        last_shot_time = current_time

    # -------------------------
    # ENEMY BULLET MOVEMENT
    # -------------------------

    for bullet in enemy_bullets[:]:

        bullet.move()
        bullet.draw(screen)

        # Check collision with player
        if bullet.rect.colliderect(player):

            enemy_bullets.remove(bullet)

            if current_time - last_player_hit >= hit_cooldown:

                lives -= 1
                last_player_hit = current_time

                player.x = 375

                if lives <= 0:
                    running = False

        elif bullet.rect.top > 600:
            enemy_bullets.remove(bullet)

    # -------------------------
    # DISPLAY PLAYER LIVES
    # -------------------------

    lives_text = font.render(
        f"Lives: {lives}", True, (255, 255, 255)
    )

    screen.blit(lives_text, (20, 15))

    # Update display
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

