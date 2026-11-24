
import pygame
import random
from enemy import Enemy
from enemy_bullet import EnemyBullet

pygame.init()
alien_images = [
    pygame.image.load("images/alien 1 transparent.png"),
    pygame.image.load("images/alien 2 transparent.png"),
    pygame.image.load("images/alien 3 transparent.png")
]

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Enemy Test")

enemies = []
bullets = []

last_shot_time = 0
shot_delay = 1200
for row in range(5):
    for col in range(7):
        x = 50 + col * 70
        y = 50 + row * 50

        image = alien_images[row % len(alien_images)]
    

        enemy = Enemy(x, y, image)
        enemies.append(enemy)

running = True
direction = 1
clock = pygame.time.Clock()


running = True
direction = 1
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Move all enemies
    for enemy in enemies:
        enemy.move(direction)

    # Check if any enemy reaches the edge
    hit_edge = (
        (direction == 1 and any(enemy.rect.right >= 500 for enemy in enemies))
        or
        (direction == -1 and any(enemy.rect.left <= 0 for enemy in enemies))
    )

    if hit_edge:
        direction *= -1

        for enemy in enemies:
            enemy.y += 20
            enemy.rect.y = enemy.y

    # Enemy shooting
    current_time = pygame.time.get_ticks()

    if current_time - last_shot_time >= shot_delay:
        shooter = random.choice(enemies)

        bullet = EnemyBullet(
            shooter.rect.centerx - 2,
            shooter.rect.bottom
        )

        bullets.append(bullet)
        last_shot_time = current_time

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)

        if bullet.rect.top > 500:
            bullets.remove(bullet)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

