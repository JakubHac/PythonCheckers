import Colors
from Puck import Puck
import State
import Singletons

class Player:
    def __init__(self, name: str, puck_color: tuple[int,int,int], on_puck_click: callable(Puck)):
        self.name = name
        self.is_white = puck_color == Colors.white_puck_color
        self.puck_color = puck_color
        self.pucks: list[Puck] = []
        self.on_puck_click: callable(Puck) = on_puck_click
        if not State.is_debug_board:
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 1:
                        if (not self.is_white and j < 3) or (self.is_white and j > 4):
                            self.add_puck((i, j))

    def add_puck(self, position_on_board: tuple[int,int]):
        puck = Puck(position_on_board, (State.puck_size, State.puck_size), self.puck_color, self.on_puck_click)
        self.pucks.append(puck)
        Singletons.GameScreen.add_puck(puck)

    def remove_puck(self, puck):
        self.pucks.remove(puck)
        puck.destroy()

    def destroy(self):
        for puck in self.pucks:
            puck.destroy()
        self.pucks.clear()
        pass