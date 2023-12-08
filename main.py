import pygame
import math
import random
from Bullet import Bullet, RegisterBullet, CapacitorBullet, OscillatorBullet, MosfetBullet
from Enemy import Enemy, ExamEnemy, QuizEnemy, ProfessorEnemy
from Item import RegisterItem, CapacitorItem, OscillatorItem, MosfetItem, StarItem
from configs import width, height
import os
from utils import binary_search, bubble_sort_with_key

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arialunicode', 20)

# 플레이어 메시지 전달을 위한 변수 설정
print_time = 0
print_text = None
printer = font.render('', True, (255, 255, 255))


# 충돌 감지 함수
def is_collision(x1, y1, x2, y2, distance=30):
    return math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2))) < distance


# 아이템 생성 함수
def create_item(level):
    if level == 0:
        return RegisterItem(random.randint(0, width - 50), -50)
    elif level == 1:
        return CapacitorItem(random.randint(0, width - 50), -50)
    elif level == 2:
        return OscillatorItem(random.randint(0, width - 50), -50)
    elif level == 3:
        return MosfetItem(random.randint(0, width - 50), -50)
    else:
        return StarItem(random.randint(0, width - 50), -50)


# 적 랜덤 생성 함수
def create_enemy(x=None, y=-50):
    enemy_type = random.choice(['exam', 'quiz'])
    if x is None:
        x = random.randint(0, width - 50)
    if enemy_type == 'exam':
        return ExamEnemy(x, y)
    elif enemy_type == 'quiz':
        return QuizEnemy(x, y)
    else:
        return Enemy(x, y)


# 총알 생성 함수
def create_bullet(player_x, player_y, level):
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
        return MosfetBullet(player_x, player_y, angle)


# 백그라운드 어둡게 조정
def darken_image(image, amount=150):
    dark = pygame.Surface((image.get_width(), image.get_height()), flags=pygame.SRCALPHA)
    dark.fill((amount, amount, amount, 0))
    image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


# users.txt에서 사용자 정보를 로드합니다
def load_users():
    if not os.path.exists('users.txt'):
        return {}
    with open('users.txt', 'r') as file:
        return {line.split()[0]: int(line.split()[1]) for line in file.readlines()}


# 사용자 점수 기록
def update_user_score(user_id, score):
    """ 사용자의 점수를 업데이트하고 파일에 기록합니다 """
    users = load_users()
    if binary_search(list(users.keys()), user_id) == -1:
        users[user_id] = 0
    users[user_id] = max(users.get(user_id, 0), score)
    with open('users.txt', 'w') as file:
        for user_id, score in users.items():
            file.write(f'{user_id} {score}\n')


# 전역 변수 설정
score = 0
user_id = ''


# 시작 화면
def start_screen():
    global user_id
    input_active = False
    global font

    # 배경 로드
    background_img = pygame.image.load('r_background.png')
    background_img = pygame.transform.scale(background_img, (width, height))

    while True:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = True
            if event.type == pygame.KEYDOWN:
                # 이름 입력하기
                if input_active:
                    if event.key == pygame.K_RETURN and user_id.isalnum():
                        game_loop()
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        user_id = user_id[:-1]
                    else:
                        user_id += event.unicode
        # 버튼 그리기
        button = pygame.Rect(100, 150, 200, 40)
        pygame.draw.rect(screen, (0, 100, 0), button)
        button_text = font.render('R관으로', True, (255, 255, 255))
        screen.blit(button_text, (button.x + 50, button.y + 5))

        # input 박스 그리기
        input_box = pygame.Rect(100, 100, 200, 40)
        pygame.draw.rect(screen, (200, 200, 200), input_box)
        if user_id:
            text_surface = font.render(user_id, True, (0, 0, 0))
        else:
            text_surface = font.render('이름', True, (150, 150, 150))

        # 캐릭터 그리기
        player = pygame.image.load('player.png')
        player = pygame.transform.scale(player, (100, 160))
        screen.blit(player, (width // 2 - 50, height // 2))

        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        pygame.display.flip()


# 게임 루프
def game_loop():
    global score
    # 게임 관련 변수 모음
    level = 3
    level_text = ['저항', '캐패시터', 'DC', '웨이퍼', '종강']
    exp = 0
    max_exp = 10

    # 플레이어 설정
    player_img = pygame.image.load('player.png')
    player_img = pygame.transform.scale(player_img, (30, 40))
    player_x, player_y = width // 2, height // 2
    player_speed = 8
    player_health = 100

    # 게임 내 오브젝트
    enemies = []
    bullets = []
    items = []
    effects = []

    boss_time = 0

    # 배경 로드
    background_img = pygame.image.load('background.png')
    background_img = pygame.transform.scale(background_img, (width, height))
    darken_image(background_img)

    # 플레이어 메시지 출력 함수
    def set_print_text(text):
        global printer, print_time, print_text
        print_text = text
        printer = font.render(text, True, (255, 255, 255))
        print_time = current_time

    while True:
        current_time = pygame.time.get_ticks()
        screen.blit(background_img, (0, 0))

        # 보스 정의
        professor = ProfessorEnemy(width // 2, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            # 총알 발사
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(create_bullet(player_x, player_y, level))

        # 플레이어 메시지 표시 로직
        if print_text and current_time - print_time < 5000:
            text_x = player_x - printer.get_width() / 2
            text_y = player_y - 60  # 플레이어 위에 표시
            screen.blit(printer, (text_x, text_y))

        if level < 5:
            # 아이템 생성
            if random.randint(1, 100) == 1:
                items.append(create_item(level))
            # 적 생성
            if random.randint(1, 60 - level * 10) == 1:
                enemies.append(create_enemy())
        else:
            # 보스 생성
            if boss_time and current_time - boss_time > 5000:
                if random.randint(1, 10) == 1:
                    for enemy in enemies:
                        if enemy.type == 'boss':
                            professor_found = enemy
                    enemies.append(create_enemy(professor_found.x, professor_found.y))



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
                items.remove(item)
                exp += 1
                # 레벨업
                if exp == max_exp:
                    level += 1
                    exp = 0
                    if level < 5:
                        set_print_text(f'{level_text[level-1]}을 얻었다!')
                    else:
                        # 보스 생성
                        set_print_text('종강이다! 앗 그런데 교수님이....')
                        boss_time = current_time
                        enemies.append(professor)
            elif item.y > height:
                items.remove(item)
            else:
                item.draw(screen)

        # 적 이동
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
                            # 게임 종료
                            if enemy.type == 'boss':
                                score = player_health
                                end_screen()
                                return None
                    break

            # 총알 충돌
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

        if player_health <= 0:
            score = player_health
            end_screen()
            return None
        # 체력, 플레이어 이름, 남은 아이템 수 표시
        user_text = font.render(f'{user_id}', True, (255, 255, 255))
        screen.blit(user_text, (width - 140, 10))
        health_text = font.render(f'학점: {player_health}', True, (255, 255, 255))
        screen.blit(health_text, (width - 140, 40))
        if level < 5:
            exp_text = font.render(f'{level_text[level]}: {exp}/{max_exp}', True, (255, 255, 255))
            screen.blit(exp_text, (width - 140, 70))

        pygame.display.flip()
        clock.tick(60)


def end_screen():
    global score
    global user_id

    # 배경 로드
    background_img = pygame.image.load('r_background.png')
    background_img = pygame.transform.scale(background_img, (width, height))
    darken_image(background_img, 100)

    if user_id:
        update_user_score(user_id, score)  # 새로운 사용자 추가

    while True:
        screen.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                # restart
                if event.key == pygame.K_r:
                    game_loop()
                    return None
                # 랭킹 보기
                if event.key == pygame.K_t:
                    ranking_screen()
                    return None

        # 스코어에 따른 그레이드와 텍스트 출력
        if score <= 0:
            grade = 'F'
            grade_text = '지금이라도 드랍하게.'
        elif score <= 30:
            grade = 'C'
            grade_text = '내년에 또 보겠군'
        elif score <= 60:
            grade = 'B'
            grade_text = '나쁘지 않구만'
        elif score <= 90:
            grade = 'A'
            grade_text = '아주 잘했네!'
        else:
            grade = 'A+'
            grade_text = '대학원 입학을 축하하네!'

        # 버튼 그리기
        button = pygame.Rect(100, 450, 200, 40)
        button_text = font.render('다시하기 (R)', True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 100, 0), button)
        screen.blit(button_text, (button.x + 40, button.y + 5))

        # 버튼 그리기
        button = pygame.Rect(100, 500, 200, 40)
        button_text = font.render('랭킹보기 (T)', True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 100, 0), button)
        screen.blit(button_text, (button.x + 40, button.y + 5))

        # 교수님 캐릭터 그리기
        professor = pygame.image.load('professor.png')
        professor = pygame.transform.scale(professor, (100, 160))
        screen.blit(professor, (width // 2 - 50, height // 2 - 80))

        # 텍스트 출력
        text_surface1 = font.render(f"{user_id} 학생!", True, (255, 255, 255))
        text_surface2 = font.render(f"자네 학점은 {grade}일세", True, (255, 255, 255))
        text_surface3 = font.render(grade_text, True, (255, 255, 255))
        screen.blit(text_surface1, (120, 100))
        screen.blit(text_surface2, (120, 130))
        screen.blit(text_surface3, (120, 160))
        pygame.display.flip()


def ranking_screen():
    global score
    global user_id
    users = load_users()
    ranking = bubble_sort_with_key(list(users.values()), list(users.keys()))
    users[user_id] = score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    return None

        # 랭킹 출력
        text_surface = font.render('RANKING', True, (255, 255, 255))
        screen.blit(text_surface, (120, 30))
        for i, (user, r_score) in enumerate(ranking.items()):
            color = (255, 255, 100) if user == user_id and r_score == score else (255 - i*10, 255 - i*10, 255 - i*10)
            text_surface = font.render(f"{i + 1}. {user}: {score}", True, color)
            screen.blit(text_surface, (120, 80 + i*30))
            if i > 10:
                break

        # 버튼 출력
        button = pygame.Rect(100, 500, 200, 40)
        button_text = font.render('다시하기 (R)', True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 100, 0), button)
        screen.blit(button_text, (button.x + 40, button.y + 5))

        pygame.display.flip()


start_screen()

pygame.quit()
