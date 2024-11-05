import pygame
import State
from pygame.rect import Rect

class Blittable:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]):
        self.pos = pos
        self.surf = pygame.Surface(size)
        self.rect = self.get_rect()
        self.rect.center = pos
        self.draw(color)

    def get_rect(self) -> Rect:
        return self.surf.get_rect()

    def draw(self, color: tuple[int, int, int]):
        self.surf.fill(color)

    def blit(self):
        State.screen.blit(self.surf, self.pos)