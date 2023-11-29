import math
import pygame
from configs import width, height
import Enemy
from Effect import CapacitorCollisionEffect, RegisterCollisionEffect, OscillatorCollisionEffect


# Bullet 클래스
class Bullet:
    def __init__(self, x, y, angle):
        self.angle = angle
        self.image = None
        self.load_image('bullet.png')
        self.x = x
        self.y = y
        self.speed = 16
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.power = 1
        self.cooltime = 0

    def load_image(self, image_url):
        self.image = pygame.image.load(image_url)
        self.image = pygame.transform.rotate(self.image, - (math.degrees(self.angle) + 90))

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.update_collision_cooltime()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def effect(self, enemy: Enemy.Enemy, enemies, effects, bullets):
        self.cooltime = 10  # 쿨타임 설정 (예: 30 프레임)
        if self in bullets:
            bullets.remove(self)

    def update_collision_cooltime(self):
        if self.cooltime > 0:
            self.cooltime -= 1


class RegisterBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.load_image('capacitor_bullet.png')

    def effect(self, enemy: Enemy.Enemy, enemies, effects, bullets):
        self.cooltime = 30  # 쿨타임 설정 (예: 30 프레임)
        effects.append(RegisterCollisionEffect(enemy.x + enemy.size[0] / 2, enemy.y + enemy.size[1] / 2))
        enemy.speed = enemy.speed / 1.3
        if self in bullets:
            bullets.remove(self)


class CapacitorBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.load_image('capacitor_bullet.png')
        self.explosion_radius = 150

    def effect(self, enemy: Enemy.Enemy, enemies, effects, bullets):
        self.cooltime = 30  # 쿨타임 설정 (예: 30 프레임)
        effects.append(CapacitorCollisionEffect(enemy.x + enemy.size[0] / 2, enemy.y + enemy.size[1] / 2))
        if self in bullets:
            bullets.remove(self)
        for other_enemy in enemies[:]:
            if math.sqrt((other_enemy.x - self.x) ** 2 + (other_enemy.y - self.y) ** 2) < self.explosion_radius:
                other_enemy.health -= 1
                if other_enemy.health <= 0:
                    enemies.remove(other_enemy)


class OscillatorBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.load_image('oscillator_bullet.png')
        self.power = 2
        self.speed = 24

    def effect(self, enemy: Enemy.Enemy, enemies, effects, bullets):
        effects.append(OscillatorCollisionEffect(enemy.x + enemy.size[0] / 2, enemy.y + enemy.size[1] / 2))
        self.cooltime = 3  # 쿨타임 설정 (예: 30 프레임)
