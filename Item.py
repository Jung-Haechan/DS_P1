import pygame
from configs import width, height


# Item 클래스
class Item:
    def __init__(self, x, y):
        self.image = pygame.image.load('item.png')
        self.size = [30, 30]
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.x = x
        self.y = y
        self.speed = 10
        self.move_direction = 1

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class RegisterItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('register_item.png')  # 폭발 아이템 이미지
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))



class CapacitorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('capacitor_item.png')  # 폭발 아이템 이미지
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))



class OscillatorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('oscillator_item.png')  # 폭발 아이템 이미지


class MosfetItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = [20, 20]
        self.image = pygame.image.load('mosfet_item.png')  # 폭발 아이템 이미지
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))

