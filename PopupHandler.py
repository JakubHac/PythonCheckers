import State
from GameState import GameState
from Popup import Popup
from Tickable import Tickable

class PopupHandler(Tickable):
    def __init__(self, popup_shown_setter: callable(bool), screen):
        self.popup_shown_setter = popup_shown_setter
        self.popup_queue = []
        self.current_popup = None
        self.screen = screen

    def clear(self):
        self.popup_queue.clear()
        self.close_popup()

    def close_popup(self):
        if self.current_popup is not None:
            self.screen.remove_blittable(self.current_popup)
        if len(self.popup_queue) > 0:
            self.current_popup = self.popup_queue.pop(0)
            self.screen.add_blittable(self.current_popup)
            self.popup_shown_setter(True)
        else:
            self.current_popup = None
            self.popup_shown_setter(False)
        pass

    def show_popup(self, text_to_display, on_close: callable=None):
        popup = Popup(text_to_display, 20, 2.0, [self.on_popup_close, on_close])
        if self.current_popup is None:
            self.current_popup = popup
            self.screen.add_blittable(self.current_popup)
            self.popup_shown_setter(True)
        else:
            self.popup_queue.append(popup)
        pass

    def on_popup_close(self, popup):
        if self.current_popup == popup:
            self.close_popup()
        else:
            print("Popup " + str(popup.to_display) + " tried to close, but it is not the current popup")

    def tick(self):
        if self.current_popup is not None:
            self.current_popup.tick()
        pass

    def popup_current_game_state(self):
        if State.game_state == GameState.WhiteChooseOwnPuck:
            self.show_popup(State.white_player.name, State.bot_move_callback)
        elif State.game_state == GameState.BlackChooseOwnPuck:
            self.show_popup(State.black_player.name, State.bot_move_callback)
        elif State.game_state == GameState.WhiteChooseMove:
            self.show_popup("Wybór ruchu dla białego pionka", State.bot_move_callback)
        elif State.game_state == GameState.BlackChooseMove:
            self.show_popup("Wybór ruchu dla czarnego pionka", State.bot_move_callback)
        elif State.game_state == GameState.WhiteChooseAttack:
            self.show_popup("Wybór ataku dla białego pionka", State.bot_move_callback)
        elif State.game_state == GameState.BlackChooseAttack:
            self.show_popup("Wybór ataku dla czarnego pionka", State.bot_move_callback)
        elif State.game_state == GameState.WhiteWon:
            self.show_popup("Wygrał biały gracz")
        elif State.game_state == GameState.BlackWon:
            self.show_popup("Wygrał czarny gracz")
        else:
            self.show_popup("404 Nieznany stan gry")