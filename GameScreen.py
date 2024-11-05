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
import Game

class GameScreen(Screen):
    def __init__(self):
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
                    color = Colors.white_tile_color
                else:
                    color = Colors.black_tile_color
                self.add_blittable(Blittable(MathUtil.board_to_screen_pos((i, j)), (State.tile_size, State.tile_size), color))

    def quit_game(self):
        Game.quit_game()
        State.active_screens.remove(self)
        State.active_screens.append(Singletons.MainMenuScreen)

    def setup_pvp_game(self):
        State.white_player = Human("Biały Gracz", True, Colors.white_puck_color, Game.puck_clicked)
        State.black_player = Human("Czarny Gracz", False, Colors.black_puck_color, Game.puck_clicked)
        Game.start()

    def setup_pve_game(self):
        human_is_white = MathUtil.random_bool()
        if human_is_white:
            State.white_player = Human("Gracz (Białe)", True, Colors.white_puck_color, Game.puck_clicked)
            State.black_player = Bot("Komputer (Czarne)", False, Colors.black_puck_color, Game.puck_clicked)
        else:
            State.white_player = Human("Komputer (Białe)", True, Colors.white_puck_color, Game.puck_clicked)
            State.black_player = Bot("Gracz (Czarne)", False, Colors.black_puck_color, Game.puck_clicked)
        Game.start()

    def add_puck(self, puck):
        self.add_clickable(puck)
        self.add_tickable(puck)

    def remove_puck(self, puck):
        self.remove_clickable(puck)
        self.remove_tickable(puck)
        pass