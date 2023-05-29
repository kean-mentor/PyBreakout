import sys
import time
from typing import List

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from levels import level_1, level_2, level_4
from sprites import Ball, Block, Paddle


def check_sides(ball: Ball, blocks: List[Block]) -> List[bool]:
    return []


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout!")

paddle = Paddle()
blocks = pygame.sprite.Group()
ball = Ball((SCREEN_WIDTH / 2, 600))

# Load block surfaces
block_surfs = []
for i in range(0, 8):
    block_surfs.append(
        pygame.image.load(f"assets/blocks/{i+1:02d}.png").convert_alpha()
    )

# Create sprites
y = 120 # 64
for row in level_4:
    x = 0
    for col in row:
        if col:
            sprite = Block(block_surfs[col - 1], (x, y), blocks)
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

    collided_blocks = pygame.sprite.spritecollide(ball, blocks, True)
    if collided_blocks:
        pass

    # Draw
    blocks.draw(screen)
    screen.blit(ball.image, ball.rect)
    screen.blit(paddle.image, paddle.rect)

    pygame.display.update()
    clock.tick(60)  # Limit FPS
