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