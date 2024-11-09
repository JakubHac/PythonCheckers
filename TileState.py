import enum
class TileState(enum.Enum):
    Empty = 0,
    White = 1,
    Black = 2,
    WhiteDame = 3,
    BlackDame = 4,
    UnknownDame = 5
    pass