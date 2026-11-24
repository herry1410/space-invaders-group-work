import pygame

class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  
