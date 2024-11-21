import pygame

import Singletons
from Clickable import Clickable
import MathUtil
import State

class PuckGhost(Clickable):
    def __init__(self, board_pos: tuple[int,int], size: int, color, on_puck_click: callable, promote_to_dame: bool, attack_pos: tuple[int,int] = None):
        pos = MathUtil.board_to_puck_pos(board_pos)
        super().__init__(pos, (size, size), color)
        self.surf.set_alpha(100)
        self.on_puck_click = on_puck_click
        self.position_on_board = board_pos
        Singletons.GameScreen.add_clickable(self)
        State.ghost_pucks.append(self)
        self.attack_pos = attack_pos
        self.promote_to_dame = promote_to_dame

    def on_click(self):
        if State.debug_mouse_clicks:
            print("PuckGhost at " + str(self.position_on_board) + " clicked")
        self.on_puck_click(self)

    def destroy(self):
        Singletons.GameScreen.remove_clickable(self)
        State.ghost_pucks.remove(self)
        pass

    def draw(self, color):
        self.surf.set_colorkey((255, 0, 0))
        self.surf.fill((255, 0, 0))
        pygame.draw.circle(self.surf, color, (State.puck_size // 2, State.puck_size // 2), State.puck_size // 2)
