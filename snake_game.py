import pygame
import time
from random import *
import sys

# 초기화
pygame.init()

# 화면 설정
screen_size = 630
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('0')

# 색상 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 캐릭터 설정
class Snake(pygame.Rect):
    def __init__(self):
        super().__init__(0, snake_size * (screen_size // (2 * snake_size)), snake_size, snake_size)
        self.overlap = snake_size // snake_speed
        self.direction = 'R'
        self.next_direction = 'R'
        self.body = [(self.x, self.y)]
        self.new_tail()

    def new_tail(self):
        while True:
            x = snake_size * randint(0, int(screen_size / snake_size) - 1)
            y = snake_size * randint(0, int(screen_size / snake_size) - 1)
            if (x, y) not in self.body:
                break
        self.tail = pygame.Rect(x, y, snake_size, snake_size)

snake_size = 30
snake_speed = 5
snake = Snake()

# 시작 시간 측정
start_time = time.time()

# 게임 루프
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 받기
    keys = pygame.key.get_pressed()

    # 다시 시작 준비
    if game_over:
        if keys[pygame.K_SPACE]:
            snake = Snake()
            start_time = time.time()
            game_over = False
        continue

    # 방향 전환 준비
    if keys[pygame.K_UP] and snake.direction != 'D':
        snake.next_direction = 'U'
    if keys[pygame.K_DOWN] and snake.direction != 'U':
        snake.next_direction = 'D'
    if keys[pygame.K_LEFT] and snake.direction != 'R':
        snake.next_direction = 'L'
    if keys[pygame.K_RIGHT] and snake.direction != 'L':
        snake.next_direction = 'R'
    
    # 칸에 맞춰 방향 전환
    if snake.x % snake_size == 0 and snake.y % snake_size == 0:
        snake.direction = snake.next_direction
    
    # 방향대로 이동
    if snake.direction == 'U':
        snake.y -= snake_speed
    if snake.direction == 'D':
        snake.y += snake_speed
    if snake.direction == 'L':
        snake.x -= snake_speed
    if snake.direction == 'R':
        snake.x += snake_speed

    # 벽에 닿으면 게임 종료
    if snake.x < 0 or snake.x + snake_size > screen_size or snake.y < 0 or snake.y + snake_size > screen_size:
        game_over = True

    # 먹이를 먹으면 꼬리 추가
    if snake.colliderect(snake.tail):
        for i in range(snake.overlap):
            snake.body.append(snake.body[-1])
        snake.new_tail()

    snake.body.insert(0, (snake.x , snake.y))
    del snake.body[-1]

    # 배경 그리기
    screen.fill(BLACK)
    
    # 캐릭터 그리기 & 꼬리와 충돌 감지
    for s in snake.body[:2 * snake.overlap + 2]:
        pygame.draw.rect(screen, RED, (s[0], s[1], snake_size, snake_size))
    for s in snake.body[2 * snake.overlap + 2:]:
        if snake.colliderect(pygame.Rect(s[0], s[1], snake_size, snake_size)):
            game_over = True
        pygame.draw.rect(screen, RED, (s[0], s[1], snake_size, snake_size))
    pygame.draw.rect(screen, GREEN, snake.tail)

    # 경과 시간 측정 & 점수 표시
    elapsed_time = (time.time() - start_time)
    if elapsed_time != 0:
        pygame.display.set_caption(str(round((((len(snake.body) // snake.overlap) ** 3) / elapsed_time))))

    # 화면 업데이트
    pygame.display.flip()

    # FPS 맞추기
    clock.tick(FPS)

    # 게임 종료 시 결과 상세 표시
    if game_over:
        pygame.display.set_caption(f'점수: {round((((len(snake.body) // snake.overlap) ** 3) / elapsed_time))} 길이: {len(snake.body) // snake.overlap} 시간: {round(elapsed_time)}')

# 게임 종료
pygame.quit()
sys.exit()