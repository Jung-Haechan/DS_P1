import math
import pygame
from configs import width, height


# Bullet 클래스
class Bullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load('bullet.png')
        self.x = x
        self.y = y
        self.speed = 16
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.power = 1

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class RegisterBullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load('bullet.png')
        self.x = x
        self.y = y
        self.speed = 16
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.power = 1

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class CapacitorBullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load('bullet.png')
        self.x = x
        self.y = y
        self.speed = 16
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.power = 1

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
