import pygame.draw

import State
from BlittableText import BlittableText
from Tickable import Tickable
from Blittable import Blittable

class Popup(Blittable, Tickable):
    def __init__(self, to_display: str, font_size: int, display_time: float, on_close: list[callable]):
        super().__init__((0, 0), (State.screen_width, State.screen_height), (0, 0, 0))
        self.surf.set_alpha(200)
        self.display_time = display_time
        if to_display is not None:
            self.text = BlittableText((State.screen_width // 2, State.screen_height // 2), font_size, (255,255,255), State.noto_font_name, to_display)
            self.to_display = to_display
        else:
            self.text = None
            self.to_display = ""
        self.on_close = on_close

    def draw(self, color):
        self.surf.set_colorkey((255, 0, 0))
        self.surf.fill((255, 0, 0))
        pygame.draw.rect(self.surf, color, (0, 0, State.screen_width, State.screen_height))

    def blit(self):
        super().blit()
        if self.text is not None:
            self.text.blit()

    def tick(self):
        passed = State.delta_time/1000.0
        self.display_time -= passed
        if self.display_time <= 0:
            for close in self.on_close:
                if close is not None:
                    close(self)
        pass

