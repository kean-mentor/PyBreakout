import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite, Group

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Block(Sprite):
    def __init__(self, surface, pos: tuple, groups: Group):
        super().__init__(groups)

        self.image = surface
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.lives = 1


class Ball(Sprite):
    def __init__(self, starting_pos: tuple, blocks: Group):
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            "assets/ball.png"
        ).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=starting_pos)
        self._pos: Vector2 = Vector2(self.rect.topleft)
        self._speed: Vector2 = Vector2(360, 360)
        self._blocks: Group = blocks
        self._old_rect = self.rect.copy()

    def _move(self, dt):
        self._pos += self._speed * dt
        self.rect.x = round(self._pos.x)
        self.rect.y = round(self._pos.y)

        # Screen boundary collision
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self._speed.x *= -1
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self._speed.y *= -1

    def _handle_block_collision(self):
        collided_blocks = pygame.sprite.spritecollide(self, self._blocks, False)
        if collided_blocks:
            # Magic number +1/-1 at self.rect's position setting is a small
            # cheat to avoid double direction change (effectively no change) if
            # two (or an even number of) blocks are hit at the same time. This
            # way only the first hit initiate the direction change.
            for block in collided_blocks:
                # top
                if (
                    self.rect.bottom >= block.rect.top
                    and self._old_rect.bottom <= block.rect.top
                ):
                    self.rect.bottom = block.rect.top - 1
                    self._pos.y = self.rect.y
                    self._speed.y *= -1

                # bottom
                if (
                    self.rect.top <= block.rect.bottom
                    and self._old_rect.top >= block.rect.bottom
                ):
                    self.rect.top = block.rect.bottom + 1
                    self._pos.y = self.rect.y
                    self._speed.y *= -1

                # left
                if (
                    self.rect.right >= block.rect.left
                    and self._old_rect.right <= block.rect.left
                ):
                    self.rect.right = block.rect.left - 1
                    self._pos.x = self.rect.x
                    self._speed.x *= -1

                # right
                if (
                    self.rect.left <= block.rect.right
                    and self._old_rect.left >= block.rect.right
                ):
                    self.rect.left = block.rect.right + 1
                    self._pos.x = self.rect.x
                    self._speed.x *= -1

                block.lives -= 1
                if block.lives < 1:
                    block.kill()

    def update(self, dt: float) -> None:
        self._old_rect = self.rect.copy()
        self._move(dt)
        self._handle_block_collision()


class Paddle(Sprite):
    def __init__(self):
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            "assets/paddle/paddle.png"
        ).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40)
        )
        self._pos: Vector2 = Vector2(self.rect.topleft)
        self._speed: int = 400
        self._moving_left = False
        self._moving_right = False

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        self._moving_left = keys[pygame.K_LEFT]
        self._moving_right = keys[pygame.K_RIGHT]

    def _move(self, dt):
        if self._moving_left:
            self._pos.x -= self._speed * dt
            self.rect.x = round(self._pos.x)

        if self._moving_right:
            self._pos.x += self._speed * dt
            self.rect.x = round(self._pos.x)

    def update(self, dt: float) -> None:
        self._handle_input()
        self._move(dt)

        # Check screen limits
        if self._pos.x <= 0:
            self._pos.x = 0
        if self._pos.x >= SCREEN_WIDTH - self.image.get_width():
            self._pos.x = SCREEN_WIDTH - self.image.get_width()
        self.rect.x = round(self._pos.x)
