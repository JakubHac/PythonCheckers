import enum
class GameState(enum.Enum):
    WhiteChooseOwnPuck = 0 #choosing a white puck to move
    BlackChooseOwnPuck = 1 #choosing a black puck to move
    WhiteChooseMove = 2 #choosing a move for a white puck
    BlackChooseMove = 3 #choosing a move for a black puck
    WhiteChooseAttack = 4 #choosing an attack for a white puck, this also forces this puck to attack until the possible attacks are over
    BlackChooseAttack = 5 #choosing an attack for a black puck, this also forces this puck to attack until the possible attacks are over
    WhiteWon = 6 #white player won
    BlackWon = 7 #black player won
    pass