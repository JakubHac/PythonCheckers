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

def get_dame_positions_before_attacks(puck, attack: list[tuple[int, int]]) -> list[tuple[int, int]]:
    start_pos = puck.position_on_board
    result = [start_pos]
    previous_pos = start_pos
    index = -1
    for tile in attack[:-1]:
        index += 1
        direction = get_direction_of_attack(previous_pos, tile)
        next_attack = attack[index + 1]
        established_pos = previous_pos
        while not is_diagonal_move(established_pos, next_attack):
            established_pos = established_pos[0] + direction[0], established_pos[1] + direction[1]
        result.append(established_pos)
        previous_pos = established_pos
    return result

def get_direction_of_attack(from_tile, attack_tile) -> tuple[int, int]:
    return MathUtil.clamp_np1(attack_tile[0] - from_tile[0]), MathUtil.clamp_np1(attack_tile[1] - from_tile[1])

def is_puck_position_promoting_to_dame(tile: tuple[int, int], puck) -> bool:
    return tile[1] == 0 if puck.is_white() else tile[1] == 7

def can_puck_become_dame_with_move(puck, others) -> bool:
    if puck.is_dame:
        return False
    if puck.is_white():
        if puck.position_on_board[1] != 1:
            #too far from promotion
            return False
        if is_tile_to_take((puck.position_on_board[0] - 1, 0), others):
            return True
        if is_tile_to_take((puck.position_on_board[0] + 1, 0), others):
            return True
    else:
        if puck.position_on_board[1] != 6:
            #too far from promotion
            return False
        if is_tile_to_take((puck.position_on_board[0] - 1, 7), others):
            return True
        if is_tile_to_take((puck.position_on_board[0] + 1, 7), others):
            return True
    return False