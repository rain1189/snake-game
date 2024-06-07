import pygame
import time
from random import *
import sys

# 초기화
pygame.init()

# 화면 설정
screen_size = 620
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Snake Game')

# 색상 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 추가 설정
class Snake(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        
    def new_tail(self):
        while True:
            x = snake.width * randint(0, int(screen_size / snake.width) - 1)
            y = snake.width * randint(0, int(screen_size / snake.width) - 1)
            if (x, y) not in snake.body:
                break
        self.tail = pygame.Rect(x, y, snake.width, snake.width)

snake = Snake(0, 40 * (screen_size // 80), 40, 40)
snake.direction = 'R'
snake.next_direction = 'R'
snake.speed = 5
snake.overlap = snake.width // snake.speed
snake.body = [(snake.x, snake.y)]
snake.new_tail()

start_time = time.time()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 게임 로직 업데이트
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != 'D':
        snake.next_direction = 'U'
    if keys[pygame.K_DOWN] and snake.direction != 'U':
        snake.next_direction = 'D'
    if keys[pygame.K_LEFT] and snake.direction != 'R':
        snake.next_direction = 'L'
    if keys[pygame.K_RIGHT] and snake.direction != 'L':
        snake.next_direction = 'R'
    
    if snake.x % snake.width == 0 and snake.y % snake.width == 0:
        snake.direction = snake.next_direction
    
    if snake.direction == 'U':
        snake.y -= snake.speed
    if snake.direction == 'D':
        snake.y += snake.speed
    if snake.direction == 'L':
        snake.x -= snake.speed
    if snake.direction == 'R':
        snake.x += snake.speed

    if snake.x < 0 or snake.x + snake.width > screen_size or snake.y < 0 or snake.y + snake.width > screen_size:
        running = False

    if snake.colliderect(snake.tail):
        for i in range(snake.overlap):
            snake.body.append(snake.body[-1])
        snake.new_tail()

    snake.body.insert(0, (snake.x , snake.y))
    del snake.body[-1]

    # 화면 그리기
    screen.fill(BLACK)
    
    # 여기에서 다양한 객체들을 그릴 수 있습니다.
    # 예: pygame.draw.rect(screen, WHITE, (x, y, width, height))
    for s in snake.body[:2 * snake.overlap + 2]:
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.width, snake.width))
    for s in snake.body[2 * snake.overlap + 2:]:
        if snake.colliderect(pygame.Rect(s[0], s[1], snake.width, snake.width)):
            running = False
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.width, snake.width))
    pygame.draw.rect(screen, GREEN, snake.tail)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 맞추기
    clock.tick(FPS)

elapsed_time = time.time() - start_time
print(f'{round(((len(snake.body) // snake.overlap) ** 3) / elapsed_time, 3)}')

# 게임 종료
pygame.quit()
sys.exit()