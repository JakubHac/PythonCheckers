from Blittable import Blittable
from Button import Button
import Colors
from Screen import Screen
import traceback
import State
import Singletons
from Human import Human

class GameScreen(Screen):
    def __init__(self):
        if Singletons.GameScreen is not None:
            print("Cannot make multiple instances of GameScreen")
            traceback.print_stack()
            pass
        super().__init__()
        Singletons.GameScreen = self
        back_button = Button((10, 10), (40, 30), Colors.white, "←", 20, State.noto_jp_font_name, Colors.black, self.quit_game)
        self.black_tile_color = (100, 100, 100)
        self.white_tile_color = (200, 200, 200)
        self.black_puck_color = (0, 0, 0)
        self.white_puck_color = (255, 255, 255)

        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.white_tile_color
                else:
                    color = self.black_tile_color
                self.add_blittable(Blittable((i * 100 + 100, j * 100 + 100), (100, 100), color))

        self.add_clickable(back_button)
        self.players = []

    def start_game(self):
        pass

    def quit_game(self):
        State.active_screens.remove(self)
        State.active_screens.append(Singletons.MainMenuScreen)

    def setup_pvp_game(self):
        self.players.clear()
        self.players.append(Human("Gracz 1"))
        self.players.append(Human("Gracz 2"))
        pass

    def setup_pve_game(self):
        self.players.clear()
        self.players.append(Human("Człowiek"))
        self.players.append(Human("Komputer"))
        pass