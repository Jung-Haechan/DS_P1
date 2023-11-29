import math
import pygame
from configs import width, height
import Enemy
from Effect import CapacitorCollisionEffect, RegisterCollisionEffect


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

    def effect(self, enemy: Enemy.Enemy, enemies, effects):
        pass


class RegisterBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.image = pygame.image.load('register_bullet.png')

    def effect(self, enemy: Enemy.Enemy, enemies, effects):
        effects.append(RegisterCollisionEffect(enemy.x + enemy.size[0] / 2, enemy.y + enemy.size[1] / 2))
        enemy.speed = enemy.speed / 1.3


class CapacitorBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.image = pygame.image.load('capacitor_bullet.png')
        self.explosion_radius = 150

    def effect(self, enemy: Enemy.Enemy, enemies, effects):
        effects.append(CapacitorCollisionEffect(enemy.x + enemy.size[0] / 2, enemy.y + enemy.size[1] / 2))
        for other_enemy in enemies[:]:
            if math.sqrt((other_enemy.x - self.x) ** 2 + (other_enemy.y - self.y) ** 2) < self.explosion_radius:
                other_enemy.health -= 1
                if other_enemy.health <= 0:
                    enemies.remove(other_enemy)
