from Button import Button
import Colors
from Screen import Screen
import traceback
import State
import Singletons

class GameScreen(Screen):
    def __init__(self):
        if Singletons.GameScreen is not None:
            print("Cannot make multiple instances of GameScreen")
            traceback.print_stack()
            pass
        super().__init__()
        Singletons.GameScreen = self
        back_button = Button((10, 10), (40, 30), Colors.white, "←", 20, State.noto_jp_font_name, Colors.black, self.quit_game)
        self.add_clickable(back_button)

    def start_game(self):
        pass

    def quit_game(self):
        State.active_screens.remove(self)
        State.active_screens.append(Singletons.MainMenuScreen)

    def setup_pvp_game(self):
        pass

    def setup_pve_game(self):
        pass