import pygame.draw

import Colors
from Tickable import Tickable
from Clickable import Clickable
import State
import MathUtil
import Singletons
import UidGenerator

class Puck(Clickable, Tickable):
    def __init__(self, position_on_board: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int], on_puck_click: callable, uid : [int] = None):
        self.position_on_board = position_on_board
        self.on_puck_click = on_puck_click
        self.is_dame = False
        self.possible_attacks = [] #list, of lists, of tuples of tiles where enemies stand that this puck can attack in a sequence
        # [] = no possible attacks
        # [ [ (1,1) ], [ (1,1) , (3,3) ] ] = 2 possible attacks, first would take out 1 enemy, second would take out 2 enemies
        if uid is not None:
            self.uid = uid
        else:
            self.uid = UidGenerator.generate_uid()
        self.color = color
        pos = MathUtil.board_to_puck_pos(position_on_board)
        super().__init__(pos, size, color)

    def move_to(self, new_position_on_board):
        self.position_on_board = new_position_on_board
        self.pos = MathUtil.board_to_puck_pos(new_position_on_board)

    def on_click(self):
        if State.debug_mouse_clicks:
            print("Puck at " + str(self.position_on_board) + " clicked")
        self.on_puck_click(self)

    def tick(self):
        pass

    def set_dame(self):
        self.is_dame = True
        self.draw(self.color)

    def draw(self, color):
        self.surf.set_colorkey((255, 0, 0))
        self.surf.fill((255, 0, 0))
        pygame.draw.circle(self.surf, color, (State.puck_size // 2, State.puck_size // 2), State.puck_size // 2)
        if self.is_dame:
            pygame.draw.circle(self.surf, (128, 128, 128), (State.puck_size // 2, State.puck_size // 2), State.puck_size // 3, 4)

    def destroy(self):
        Singletons.GameScreen.remove_puck(self)

    def is_same_puck(self, puck):
        return self.uid == puck.uid

    def is_ally(self, puck):
        return self.color == puck.color

    def is_enemy(self, puck):
        return not self.is_ally(puck)

    def is_white(self):
        return self.color == Colors.white_puck_color

    def is_black(self):
        return self.color == Colors.black_puck_color

    def __copy__(self):
        return Puck(self.position_on_board, (State.puck_size, State.puck_size), self.color, self.on_puck_click, self.uid)

    def __deepcopy__(self, memo):
        result = self.__copy__()
        memo[id(self)] = result
        return result