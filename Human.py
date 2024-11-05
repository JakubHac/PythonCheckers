from Player import Player

class Human(Player):
    def __init__(self, name: str, is_white: bool, puck_color: tuple[int, int, int], on_puck_click: callable):
        super().__init__(name, is_white, puck_color, on_puck_click)
        pass
    pass
