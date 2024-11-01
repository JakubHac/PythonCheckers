from Blittable import Blittable
from Button import Button
import Colors
from Screen import Screen
import traceback
import State
import Singletons
from Human import Human
from Bot import Bot
import MathUtil
from Game import Game

class GameScreen(Screen):
    def __init__(self):
        #consts
        self.white_tile_color = (220, 180, 120)
        self.black_tile_color = (120, 55, 25)
        self.white_puck_color = (255, 255, 255)
        self.black_puck_color = (0, 0, 0)
        #init
        if Singletons.GameScreen is not None:
            print("Cannot make multiple instances of GameScreen")
            traceback.print_stack()
            pass
        super().__init__()
        Singletons.GameScreen = self
        #ui
        back_button = Button((10, 10), (40, 30), Colors.white, "←", 20, State.noto_jp_font_name, Colors.black, self.quit_game)
        self.add_clickable(back_button)
        #game setup
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.white_tile_color
                else:
                    color = self.black_tile_color
                self.add_blittable(Blittable(MathUtil.board_to_screen_pos((i, j)), (State.tile_size, State.tile_size), color))
        self.game = Game()

    def start_game(self):
        self.game.start()
        pass

    def quit_game(self):
        State.active_screens.remove(self)
        State.active_screens.append(Singletons.MainMenuScreen)

    def setup_pvp_game(self):
        State.white_player = Human("Biały Gracz", True, self.white_puck_color)
        State.black_player = Human("Czarny Gracz", False, self.black_puck_color)
        pass

    def setup_pve_game(self):
        human_is_white = MathUtil.random_bool()
        if human_is_white:
            State.white_player = Human("Gracz (Białe)", True, self.white_puck_color)
            State.black_player = Bot("Komputer (Czarne)", False, self.black_puck_color)
        else:
            State.white_player = Human("Komputer (Białe)", True, self.white_puck_color)
            State.black_player = Bot("Gracz (Czarne)", False, self.black_puck_color)
        pass

    def add_puck(self, puck):
        self.add_clickable(puck)
        self.add_tickable(puck)
        pass

    def remove_puck(self, puck):
        self.remove_clickable(puck)
        self.remove_tickable(puck)
        pass