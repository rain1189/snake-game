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
    def __init__(self, size):
        super().__init__(0, size * (screen_size // (2 * size)), size, size)
        
    def new_tail(self):
        while True:
            x = snake.size[0] * randint(0, int(screen_size / snake.size[0]) - 1)
            y = snake.size[0] * randint(0, int(screen_size / snake.size[0]) - 1)
            if (x, y) not in snake.body:
                break
        self.tail = pygame.Rect(x, y, snake.size[0], snake.size[0])

snake = Snake(30)
snake.direction = 'R'
snake.next_direction = 'R'
snake.speed = 5
snake.overlap = snake.size[0] // snake.speed
snake.body = [(snake.x, snake.y)]
snake.new_tail()

# 시작 시간 측정
start_time = time.time()

# 게임 루프
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 죽으면 멈추기
    if game_over:
        pygame.display.set_caption(f'점수: {round((((len(snake.body) // snake.overlap) ** 3) / elapsed_time))} 길이: {len(snake.body) // snake.overlap} 시간: {round(elapsed_time)}')
        continue

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
    
    if snake.x % snake.size[0] == 0 and snake.y % snake.size[0] == 0:
        snake.direction = snake.next_direction
    
    if snake.direction == 'U':
        snake.y -= snake.speed
    if snake.direction == 'D':
        snake.y += snake.speed
    if snake.direction == 'L':
        snake.x -= snake.speed
    if snake.direction == 'R':
        snake.x += snake.speed

    if snake.x < 0 or snake.x + snake.size[0] > screen_size or snake.y < 0 or snake.y + snake.size[0] > screen_size:
        game_over = True

    if snake.colliderect(snake.tail):
        for i in range(snake.overlap):
            snake.body.append(snake.body[-1])
        snake.new_tail()

    snake.body.insert(0, (snake.x , snake.y))
    del snake.body[-1]

    # 화면 그리기
    screen.fill(BLACK)
    
    # 캐릭터 그리기
    for s in snake.body[:2 * snake.overlap + 2]:
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.size[0], snake.size[0]))
    for s in snake.body[2 * snake.overlap + 2:]:
        if snake.colliderect(pygame.Rect(s[0], s[1], snake.size[0], snake.size[0])):
            game_over = True
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.size[0], snake.size[0]))
    pygame.draw.rect(screen, GREEN, snake.tail)

    # 경과 시간 측정 및 점수 표시
    elapsed_time = (time.time() - start_time)
    if elapsed_time != 0:
        pygame.display.set_caption(str(round((((len(snake.body) // snake.overlap) ** 3) / elapsed_time))))

    # 화면 업데이트
    pygame.display.flip()

    # FPS 맞추기
    clock.tick(FPS)

# 게임 종료
pygame.quit()
sys.exit()