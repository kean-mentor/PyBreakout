import sys
import time
from typing import List

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from levels import level_1, level_2, level_4
from sprites import Ball, Block, Paddle


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout!")

paddle = Paddle()
blocks = pygame.sprite.Group()
ball = Ball((SCREEN_WIDTH / 2, 600), blocks)

# Create sprites
y = 64
for row in level_2:
    x = 0
    for col in row:
        if col:
            sprite = Block(col, (x, y), blocks)
        x += 73
    y += 33

# Start game loop
prev_time = time.time()
while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")

    ball.update(dt)
    paddle.update(dt)

    if pygame.sprite.collide_rect(ball, paddle):
        ball._speed.y *= -1

    # Draw
    blocks.draw(screen)
    screen.blit(ball.image, ball.rect)
    screen.blit(paddle.image, paddle.rect)

    pygame.display.update()
    clock.tick(60)  # Limit FPS
