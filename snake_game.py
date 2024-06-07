import pygame
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

snake = Snake(0, 20 * (screen_size // 40), 20, 20)
snake.body = [(snake.x, snake.y)]
snake.direction = ['R', 'D', 'L', 'U']
snake.speed = 5
snake.new_tail()

released = [True, True]

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 게임 로직 업데이트
    if snake.x % snake.width == 0 and snake.y % snake.width == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if released[0]:
                snake.direction.insert(0, snake.direction[-1])
                del snake.direction[-1]
                released[0] = False
        else:
            released[0] = True
        if keys[pygame.K_RIGHT]:
            if released[1]:
                snake.direction.append(snake.direction[0])
                del snake.direction[0]
                released[1] = False 
        else:
            released[1] = True
    
    if snake.direction[0] == 'U':
        snake.y -= snake.speed
    if snake.direction[0] == 'D':
        snake.y += snake.speed
    if snake.direction[0] == 'L':
        snake.x -= snake.speed
    if snake.direction[0] == 'R':
        snake.x += snake.speed

    if snake.x < 0 or snake.x + snake.width > screen_size or snake.y < 0 or snake.y + snake.width > screen_size:
        running = False

    if snake.colliderect(snake.tail):
        for i in range(4):
            snake.body.append((-20,-20))
        snake.new_tail()

    snake.body.insert(0, (snake.x , snake.y))
    del snake.body[-1]

    # 화면 그리기
    screen.fill(BLACK)
    
    # 여기에서 다양한 객체들을 그릴 수 있습니다.
    # 예: pygame.draw.rect(screen, WHITE, (x, y, width, height))
    for s in snake.body[:8]:
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.width, snake.width))
    for s in snake.body[8:]:
        if snake.colliderect(pygame.Rect(s[0], s[1], snake.width, snake.width)):
            running = False
            break
        pygame.draw.rect(screen, RED, (s[0], s[1], snake.width, snake.width))
    pygame.draw.rect(screen, GREEN, snake.tail)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 맞추기
    clock.tick(FPS)

# 게임 종료
pygame.quit()
sys.exit()
