import State
from Blittable import Blittable

class Clickable(Blittable):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)

    def check_click(self, mouse_pos):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        if self.rect.collidepoint(mouse_pos):
            self.on_click()

    def on_click(self):
        if State.debug_mouse_clicks:
            print("Clickable at " + str(self.rect.center) + " clicked")
