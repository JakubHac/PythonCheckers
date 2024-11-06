from Puck import Puck
import State
import Singletons

class Player:
    def __init__(self, name: str, is_white: bool, puck_color: tuple[int,int,int], on_puck_click: callable):
        self.name = name
        self.is_white = is_white
        self.puck_color = puck_color
        self.pucks = []
        if not State.is_debug_board:
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 1:
                        if (not self.is_white and j < 3) or (self.is_white and j > 4):
                            self.pucks.append(Puck((i, j), (State.puck_size, State.puck_size), self.puck_color, on_puck_click))
                            Singletons.GameScreen.add_puck(self.pucks[-1])

    def destroy(self):
        for puck in self.pucks:
            puck.destroy()
        pass