import State
from Clickable import Clickable
from BlittableText import BlittableText

class Button(Clickable):
    def __init__(self, pos, size, color, to_display, font_size, font_name, text_color, on_click):
        super().__init__(pos, size, color)
        if to_display is not None:
            self.text = BlittableText((pos[0] + size[0]/2, pos[1] + size[1]/2), font_size, text_color, font_name, to_display)
            self.to_display = to_display
        else:
            self.text = None
            self.to_display = ""
        self.on_click = on_click

    def on_click(self):
        if State.debug_mouse_clicks:
            print("Button " + self.to_display + " at " + str(self.rect.center) + " clicked")
        self.on_click()

    def blit(self):
        super().blit()
        if self.text is not None:
            self.text.blit()