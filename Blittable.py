import pygame
import State

class Blittable:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.surf = pygame.Surface(size)
        self.rect = self.get_rect()
        self.rect.center = pos
        self.draw(color)

    def get_rect(self):
        return self.surf.get_rect()

    def draw(self, color):
        self.surf.fill(color)

    def blit(self):
        State.screen.blit(self.surf, self.pos)