import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite, Group

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Block(Sprite):
    def __init__(self, surface, pos: tuple, groups: Group):
        super().__init__(groups)

        self.image = surface
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        # self.lives = 1


class Ball(Sprite):
    def __init__(self, starting_pos: tuple):
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            "assets/ball.png"
        ).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=starting_pos)
        self._pos: Vector2 = Vector2(self.rect.topleft)
        self._speed: Vector2 = Vector2(360, 360)

    def _move(self, dt):
        self._pos += self._speed * dt
        self.rect.x = round(self._pos.x)
        self.rect.y = round(self._pos.y)

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self._speed.x *= -1
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self._speed.y *= -1

    def update(self, dt: float) -> None:
        self._move(dt)


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
