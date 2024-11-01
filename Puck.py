import pygame.draw

from Tickable import Tickable
from Clickable import Clickable
import State
import MathUtil
import Singletons

class Puck(Clickable, Tickable):
    def __init__(self, position_on_board, size, color, on_puck_click):
        self.position_on_board = position_on_board
        self.on_puck_click = on_puck_click
        self.is_dame = False
        self.possible_attacks = [] #list, of lists, of tuples of tiles where this pucks needs to move to execute an attack
        #[] = no possible attacks
        #[ [ (2,2) ], [ (2,2) , (4,4) ] ] = 2 possible attacks, first would take out 1 enemy, second would take out 2 enemies
        pos = MathUtil.board_to_puck_pos(position_on_board)
        super().__init__(pos, size, color)

    def on_click(self):
        if State.debug_mouse_clicks:
            print("Puck at " + str(self.rect.center) + " clicked")
        self.on_puck_click(self)

    def tick(self):
        pass

    def draw(self, color):
        self.surf.set_colorkey((255, 0, 0))
        self.surf.fill((255, 0, 0))
        pygame.draw.circle(self.surf, color, (State.puck_size // 2, State.puck_size // 2), State.puck_size // 2)
        if self.is_dame:
            pygame.draw.circle(self.surf, (128, 128, 128), (State.puck_size // 2, State.puck_size // 2), State.puck_size // 3, 4)

    def destroy(self):
        Singletons.GameScreen.remove_puck(self)