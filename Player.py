from Puck import Puck
import State
import Singletons

class Player:
    def __init__(self, name, is_white, puck_color):
        self.name = name
        self.is_white = is_white
        self.puck_color = puck_color
        self.pucks = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    if (not self.is_white and j < 3) or (self.is_white and j > 4):
                        self.pucks.append(Puck((i, j), (State.puck_size, State.puck_size), self.puck_color, self.on_puck_click))
                        Singletons.GameScreen.add_puck(self.pucks[-1])

    def on_puck_click(self, puck):
        pass
