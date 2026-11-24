
import pygame

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (40, 40))
        self.width = 40
        self.height = 40

        self.rect = self.image.get_rect(
            topleft=(self.x, self.y)
        )

        self.speed = 0.5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, direction):
        self.x += direction * self.speed
        self.rect.x = self.x

