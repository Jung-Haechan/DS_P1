import pygame
import math
import random
from Bullet import Bullet
from Enemy import Enemy
from Item import Register, Capacitor
from configs import width, height


# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


# 충돌 감지 함수
def is_collision(x1, y1, x2, y2, distance=27):
    return math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2))) < distance

# 아이템 랜덤 생성 함수
def create_random_item():
    if random.choice([True, False]):
        return Register(random.randint(0, width - 50), -50)
    else:
        return Capacitor(random.randint(0, width - 50), -50)


# 플레이어 설정
player_img = pygame.image.load('player.png')
player_x, player_y = width // 2, height // 2
player_speed = 8
player_health = 100

# 게임 변수
enemies = []
bullets = []
items = []
item_active = False
item_effect_duration = 5000
last_item_time = 0

running = True
while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            angle = math.atan2(my - player_y, mx - player_x)
            bullets.append(Bullet(player_x, player_y, angle))

    # 아이템 생성
    if random.randint(1, 100) == 1 and not items:
        items.append(create_random_item())

    # 아이템 효과 시간 확인
    if item_active and current_time - last_item_time > item_effect_duration:
        item_active = False

    # 플레이어 이동
    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_d] - keys[pygame.K_a]) * player_speed
    player_y += (keys[pygame.K_s] - keys[pygame.K_w]) * player_speed
    player_x = max(0, min(width - 50, player_x))
    player_y = max(0, min(height - 50, player_y))

    # 아이템 획득 체크 및 이동
    for item in items[:]:
        item.move()
        if is_collision(player_x, player_y, item.x, item.y, 50):
            item_active = True
            last_item_time = pygame.time.get_ticks()
            items.remove(item)
        elif item.y > height:
            items.remove(item)
        else:
            item.draw(screen)

    # 적 생성 및 이동
    if random.randint(1, 50) == 1:
        enemies.append(Enemy(random.randint(0, width - 50), -50))
    for enemy in enemies[:]:
        enemy.move()
        if enemy.y > height:
            player_health -= 5
            enemies.remove(enemy)
        else:
            enemy.draw(screen)

    # 총알 이동 및 충돌 체크
    for bullet in bullets[:]:
        bullet.move()
        for enemy in enemies[:]:
            if is_collision(enemy.x, enemy.y, bullet.x, bullet.y):
                enemy.health -= bullet.power
                bullets.remove(bullet)
                enemy.health -= 1

        if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
            bullets.remove(bullet)
        else:
            bullet.draw(screen)

    # 플레이어 그리기
    screen.blit(player_img, (player_x, player_y))

    # 체력 표시
    health_text = font.render(f'Health: {player_health}', True, (255, 255, 255))
    screen.blit(health_text, (width - 150, 10))

    pygame.display.flip()
    clock.tick(60)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
