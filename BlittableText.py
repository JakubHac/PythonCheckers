import State
import pygame
from Blittable import Blittable

class BlittableText(Blittable):
    def __init__(self, pos, size, color, font_name, to_display):
        self.font = pygame.font.Font(font_name, size)
        self.text = self.font.render(to_display, True, color)
        super().__init__(pos, (size,size), color)

    def get_rect(self):
        return self.text.get_rect()

    def draw(self, color):
        pass

    def blit(self):
        self.rect.center = self.pos
        State.screen.blit(self.text, self.rect)