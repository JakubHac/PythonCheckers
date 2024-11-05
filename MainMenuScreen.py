import traceback
import State
import Colors
from BlittableText import BlittableText
from Screen import Screen
from Button import Button
from GameScreen import GameScreen
import Singletons

def quit_game():
    State.close_requested = True

class MainMenuScreen(Screen):
    def __init__(self):
        if Singletons.MainMenuScreen is not None:
            print("Cannot make multiple instances of MainMenuScreen")
            traceback.print_stack()
            pass
        super().__init__()
        Singletons.MainMenuScreen = self
        footer_size = 20
        button_size = (250, 50)
        button_x = State.screen_width / 2 - button_size[0] / 2
        button_y = State.screen_height / 2
        button_y_offset = 100
        button_font_size = 20

        title_text = BlittableText((State.screen_width / 2, 250), 50, Colors.white, State.noto_font_name, "Warcaby")
        footer_text = BlittableText((State.screen_width / 2, State.screen_height - footer_size), footer_size, Colors.white, State.noto_font_name, "Jakub Hac 19755")
        start_pvp_button = Button((button_x, button_y - button_y_offset), button_size, Colors.white, "Człowiek vs Człowiek", button_font_size, State.noto_font_name, Colors.black, self.start_pvp_game)
        start_pve_button = Button((button_x, button_y), button_size, Colors.white, "Człowiek vs Maszyna", button_font_size, State.noto_font_name, Colors.black, self.start_pve_game)
        quit_button = Button((button_x, button_y + button_y_offset), button_size, Colors.white, "Zamknij", button_font_size, State.noto_font_name, Colors.black, quit_game)
        self.add_blittable(title_text)
        self.add_blittable(footer_text)
        self.add_clickable(start_pvp_button)
        self.add_clickable(start_pve_button)
        self.add_clickable(quit_button)

    def start_pvp_game(self):
        if Singletons.GameScreen is None:
            GameScreen()

        Singletons.GameScreen.setup_pvp_game()
        State.active_screens.append(Singletons.GameScreen)
        State.active_screens.remove(self)
        pass

    def start_pve_game(self):
        if Singletons.GameScreen is None:
            GameScreen()

        Singletons.GameScreen.setup_pve_game()
        State.active_screens.append(Singletons.GameScreen)
        State.active_screens.remove(self)
        pass