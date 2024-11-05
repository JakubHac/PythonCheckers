import State
import random

def board_to_screen_pos(board_pos: tuple[int,int]) -> tuple[int,int]:
    return board_pos[0] * State.tile_size + State.tile_offset_from_screen, board_pos[1] * State.tile_size + State.tile_offset_from_screen

def board_to_puck_pos(board_pos: tuple[int,int]) -> tuple[int,int]:
    pos = board_to_screen_pos(board_pos)
    offset = (State.tile_size - State.puck_size) / 2
    return pos[0] + offset, pos[1] + offset

def random_bool() -> bool:
    return random.choice([True, False])

def clamp(minvalue: int, value: int, maxvalue: int) -> int:
    return max(minvalue, min(value, maxvalue))

def clamp01(value: int) -> int:
    return clamp(0, value, 1)

def clamp_np1(value: int) -> int:
    return clamp(-1, value, 1)