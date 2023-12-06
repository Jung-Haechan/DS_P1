import pygame
import math
import random
from Bullet import Bullet, RegisterBullet, CapacitorBullet, OscillatorBullet, MosfetBullet
from Enemy import Enemy, ExamEnemy, QuizEnemy
from Item import RegisterItem, CapacitorItem, OscillatorItem, MosfetItem
from configs import width, height


# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

point = 0

print_time = 0
print_text = None


# 충돌 감지 함수
def is_collision(x1, y1, x2, y2, distance=30):
    return math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2))) < distance


# 아이템 랜덤 생성 함수
def create_item():
    if level == 0:
        return RegisterItem(random.randint(0, width - 50), -50)
    elif level == 1:
        return CapacitorItem(random.randint(0, width - 50), -50)
    elif level == 2:
        return OscillatorItem(random.randint(0, width - 50), -50)
    elif level == 3:
        return MosfetItem(random.randint(0, width - 50), -50)
    else:
        return MosfetItem(random.randint(0, width - 50), -50)


def create_enemy():
    enemy_type = random.choice(['exam', 'quiz'])
    if enemy_type == 'exam':
        return ExamEnemy(random.randint(0, width - 50), -50)
    elif enemy_type == 'quiz':
        return QuizEnemy(random.randint(0, width - 50), -50)
    else:
        return Enemy(random.randint(0, width - 50), -50)


def create_bullet(player_x, player_y):
    mx, my = pygame.mouse.get_pos()
    angle = math.atan2(my - player_y, mx - player_x)
    if level == 0:
        return Bullet(player_x, player_y, angle)
    elif level == 1:
        return RegisterBullet(player_x, player_y, angle)
    elif level == 2:
        return CapacitorBullet(player_x, player_y, angle)
    elif level == 3:
        return OscillatorBullet(player_x, player_y, angle)
    elif level == 4:
        return MosfetBullet(player_x, player_y, angle)
    else:
        return None


level = 4
exp = 0
max_exp = 10

background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (width, height))

# 플레이어 설정
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (30, 40))
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
effects = []

running = True
while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(create_bullet(player_x, player_y))

    screen.blit(background_img, (0, 0))
    #
    # # 텍스트 표시 로직
    # if print_text and current_time - print_time > 5000:
    #     print_text = None
    #     print_time = 0

    # 아이템 생성
    if random.randint(1, 50) == 1:
        items.append(create_item())

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
        if is_collision(player_x, player_y, item.x, item.y, 20):
            item_active = True
            last_item_time = pygame.time.get_ticks()
            items.remove(item)
            exp += 1
            if exp == max_exp:
                level += 1
                exp = 0
        elif item.y > height:
            items.remove(item)
        else:
            item.draw(screen)

    # 적 생성 및 이동
    if random.randint(1, 60 - level*10) == 1:
        enemies.append(create_enemy())
    for enemy in enemies[:]:
        enemy.move()
        if enemy.y > height:
            player_health -= 5
            if enemy in enemies:
                enemies.remove(enemy)
        else:
            enemy.draw(screen)

    # 총알 이동 및 충돌 체크
    for bullet in bullets[:]:
        bullet.move()
        for enemy in enemies[:]:
            if is_collision(enemy.x, enemy.y, bullet.x, bullet.y, enemy.size[0]) and bullet.cooltime == 0:
                enemy.health -= bullet.power
                bullet.effect(enemy, enemies, effects, bullets)
                if enemy.health <= 0:
                    if enemy in enemies:
                        enemies.remove(enemy)
                        point += 1
                break

        if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
            if bullet in bullets:
                bullets.remove(bullet)
        else:
            bullet.draw(screen)

    # 이펙트 그리기
    for effect in effects[:]:
        effect.update()
        if effect.finished:
            effects.remove(effect)
        else:
            effect.draw(screen)

    # 플레이어 그리기
    screen.blit(player_img, (player_x, player_y))

    # 체력 표시
    health_text = font.render(f'Health: {player_health}', True, (0, 0, 0))
    exp_text = font.render(f'Item: {exp}/{max_exp}', True, (0, 0, 0))
    screen.blit(health_text, (width - 150, 10))
    screen.blit(exp_text, (width - 150, 30))

    pygame.display.flip()
    clock.tick(60)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
