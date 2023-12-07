import pygame
from configs import width, height
import random



# Enemy 클래스
class Enemy:
    def __init__(self, x, y):
        self.size = [30, 30]
        self.x = x
        self.y = y
        self.health = 5
        self.max_health = 5
        self.speed = 3
        self.direction = 1
        self.type = 'enemy'

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
        self.speed = 5
        self.max_health = 3
        self.health = 3
        self.image = pygame.image.load('quiz_enemy.png')
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))


class ProfessorEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 4
        self.max_health = 50
        self.health = self.max_health
        self.size = [30, 40]
        self.image = pygame.image.load('professor.png')
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.type = 'boss'

    def move(self):
        dir_change = random.randint(1, 40) == 1
        if self.x < 50 or self.x > width - 50:
            dir_change = True
        if dir_change:
            print(self.x)
            self.direction = - self.direction
            self.x += self.speed * self.direction

        self.x += self.speed * self.direction

