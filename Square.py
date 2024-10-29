from Clickable import Clickable
import State
from Tickable import Tickable

class Square(Clickable, Tickable):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)
        self.desired_y = pos[1]

    def on_click(self):
        if State.debug_mouse_clicks:
            print("Square at " + str(self.rect.center) + " clicked")
        self.desired_y += 100

    def tick(self):
        to_travel = 5 * State.delta_time/1000
        dist = self.desired_y - self.pos[1]
        if dist <= to_travel:
            self.pos = (self.pos[0], self.desired_y)
            pass
        self.pos = (self.pos[0], self.pos[1] + to_travel)
