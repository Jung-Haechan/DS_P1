import pygame
from configs import width, height


# Enemy 클래스
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('enemy.png')
        self.size = [30, 30]
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.x = x
        self.y = y
        self.health = 5
        self.max_health = 5
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        # 체력 바의 길이와 높이
        bar_length = self.size[0]
        bar_height = 5
        # 체력에 비례하여 채워질 길이 계산
        fill = (self.health / self.max_health) * bar_length
        # 체력 바 테두리
        border_rect = pygame.Rect(self.x, self.y - 10, bar_length, bar_height)
        # 체력 바 채우기
        fill_rect = pygame.Rect(self.x, self.y - 10, fill, bar_height)
        # 체력 바 그리기
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)  # 빨간색으로 채우기
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)  # 테두리


class ExamEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('exam_enemy.png')
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))


class QuizEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('quiz_enemy.png')
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
