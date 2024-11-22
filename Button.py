import State
from Clickable import Clickable
from BlittableText import BlittableText

class Button(Clickable):
    def __init__(self, pos, size, color, to_display, font_size: int, font_name: str, text_color: tuple[int,int,int], on_click: callable):
        super().__init__(pos, size, color)
        if to_display is not None:
            self.text = BlittableText((pos[0] + size[0]//2, pos[1] + size[1]//2), font_size, text_color, font_name, to_display)
            self.to_display = to_display
        else:
            self.text = None
            self.to_display = ""
        self.on_click_action = on_click

    def on_click(self):
        if State.is_game_popup_shown:
            return  # do not allow any actions when popup is shown
        if State.debug_mouse_clicks:
            print("Button " + self.to_display + " at " + str(self.rect.center) + " clicked")
        self.on_click_action()

    def blit(self):
        super().blit()
        if self.text is not None:
            self.text.blit()