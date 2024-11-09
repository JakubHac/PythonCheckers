from Player import Player

class Bot(Player):
    def __init__(self, name: str, puck_color: tuple[int, int, int], on_puck_click: callable):
        super().__init__(name, puck_color, on_puck_click)
        pass
    pass