from Clickable import Clickable
import MathUtil
import State

class PuckGhost(Clickable):
    def __init__(self, board_pos, size, color, on_puck_click):
        pos = MathUtil.board_to_puck_pos(board_pos)
        super().__init__(pos, size, color)
        self.surf.set_alpha(150)
        self.on_puck_click = on_puck_click

    def on_click(self):
        if State.debug_mouse_clicks:
            print("PuckGhost at " + str(self.rect.center) + " clicked")
        self.on_puck_click(self)
        pass
