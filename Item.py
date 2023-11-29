import pygame
from configs import width, height


# Item 클래스
class Item:
    def __init__(self, x, y):
        self.image = pygame.image.load('item.png')
        self.x = x
        self.y = y
        self.speed = 4
        self.zigzag_speed = 7  # 지그재그 이동 속도
        self.zigzag_width = 20  # 지그재그 너비
        self.move_direction = 1

    def move(self):
        self.y += self.speed
        self.x += self.move_direction * self.zigzag_speed
        # 지그재그 이동 방향 변경
        if self.x <= 0 or self.x >= width - self.image.get_width():
            self.move_direction *= -1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class RegisterItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('register_item.png')  # 폭발 아이템 이미지


class CapacitorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('capacitor_item.png')  # 폭발 아이템 이미지
