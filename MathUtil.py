import State
import random

def board_to_screen_pos(board_pos):
    return board_pos[0] * State.tile_size + State.tile_offset_from_screen, board_pos[1] * State.tile_size + State.tile_offset_from_screen

def board_to_puck_pos(board_pos):
    pos = board_to_screen_pos(board_pos)
    offset = (State.tile_size - State.puck_size) / 2
    return pos[0] + offset, pos[1] + offset

def random_bool():
    return random.choice([True, False])