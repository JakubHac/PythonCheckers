import traceback

import MathUtil

def is_tile_empty(tile: tuple[int, int], pucks) -> bool:
    if any([puck for puck in pucks if puck.position_on_board == tile]):
        return False
    return True

def is_tile_on_board(tile: tuple[int, int]) -> bool:
    return 0 <= tile[0] < 8 and 0 <= tile[1] < 8

def move_puck_after_attack(puck, tile: tuple[int, int]):
    puck.move_to(get_puck_position_after_attack(puck, tile))
    pass

def get_puck_position_after_attack(puck, tile: tuple[int, int]) -> tuple[int, int]:
    attack_direction = (MathUtil.clamp_np1(tile[0] - puck.position_on_board[0]), MathUtil.clamp_np1(tile[1] - puck.position_on_board[1]))
    tile_after_attack = (tile[0] + attack_direction[0], tile[1] + attack_direction[1])
    return tile_after_attack

def is_attack_valid(from_tile, to_tile, is_dame, allies, enemies) -> bool:
    x_change = to_tile[0] - from_tile[0]
    y_change = to_tile[1] - from_tile[1]
    return is_attack_direction_valid(from_tile, x_change, y_change, is_dame, allies, enemies)

def is_tile_to_take(tile: tuple[int, int], pucks) -> bool:
    if not is_tile_on_board(tile):
        return False
    if not is_tile_empty(tile, pucks):
        return False
    return True

def is_diagonal_move(from_tile, to_tile) -> bool:
    x_change = to_tile[0] - from_tile[0]
    y_change = to_tile[1] - from_tile[1]
    return abs(x_change) == abs(y_change)

def is_attack_direction_valid(from_tile, x_change: int, y_change: int, is_dame, allies, enemies) -> bool:
    attack_self: bool = x_change == 0 and y_change == 0
    if attack_self:
        print("Invalid tile for attack")
        # TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False
    single_axis_move: bool = abs(x_change) == 0 or abs(y_change) == 0
    if single_axis_move:
        print("Invalid tile for attack")
        # TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False

    diagonal_move: bool = abs(x_change) == abs(y_change)
    if not diagonal_move:
        print("Invalid tile for attack")
        # TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False

    long_move: bool = abs(x_change) > 1 or abs(y_change) > 1
    if long_move and not is_dame:
        print("Invalid tile for attack")
        # TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False

    tile_pos = (from_tile[0] + x_change, from_tile[1] + y_change)
    next_tile_pos = (tile_pos[0] + MathUtil.clamp_np1(x_change), tile_pos[1] + MathUtil.clamp_np1(y_change))
    if not is_tile_on_board(tile_pos):
        # out of bounds, attack not possible, not an exception, expected when checking directions
        return False
    if not is_tile_to_take(next_tile_pos, allies + enemies):
        # out of bounds, attack not possible, not an exception, expected when checking directions
        return False

    # find enemy on the tile
    if not any(e.position_on_board == tile_pos for e in enemies):
        return False

    return True
