import copy
import traceback

import BoardOperations
import State
from Puck import Puck

def calculate_possible_attacks(ally_pucks: list[Puck], enemy_pucks: list[Puck]) -> list[Puck]:  # and sort them in descending order
    # clear possible attacks
    [puck.possible_attacks.clear() for puck in ally_pucks]
    # for each puck, get first possible attacks
    ally_pucks_that_can_attack = [puck for puck in ally_pucks if count_puck_possible_single_attacks_from_current_tile(puck, ally_pucks, enemy_pucks)]
    ally_pucks_that_cannot_attack = [puck for puck in ally_pucks if len(puck.possible_attacks) == 0]
    # try to extend all attacks, until no attack can be extended
    pucks_with_extendable_attacks = ally_pucks_that_can_attack.copy()
    extend_attacks_of_length = 1
    while True:
        pucks_with_extended_attacks = []
        for puck in pucks_with_extendable_attacks:
            if extend_attacks(puck, ally_pucks, enemy_pucks, pucks_with_extended_attacks):
                pucks_with_extended_attacks.append(puck)
        if len(pucks_with_extended_attacks) == 0:
            break
        extend_attacks_of_length += 1
        pucks_with_extendable_attacks = pucks_with_extended_attacks

    # sort by the longest attack
    ally_pucks_that_can_attack.sort(key=lambda x: max(len(attack) for attack in x.possible_attacks), reverse=True)
    out_ally_pucks = ally_pucks_that_can_attack
    out_ally_pucks += ally_pucks_that_cannot_attack
    return out_ally_pucks

def this_puck_has_longest_attack(puck: Puck, allies_sorted_by_possible_attacks: list[Puck]) -> tuple[bool, bool]:
    try:
        max_length_of_allied_attack = max(max(len(attack) for attack in allied_puck.possible_attacks) for allied_puck in allies_sorted_by_possible_attacks)
    except ValueError:
        max_length_of_allied_attack = 0
    try:
        max_length_of_our_attack = max(len(attack) for attack in puck.possible_attacks)
    except ValueError:
        max_length_of_our_attack = 0
    return max_length_of_our_attack == max_length_of_allied_attack, max_length_of_allied_attack > 0

def extend_attacks(puck: Puck, allies_before_any_attack: list[Puck], enemies_before_any_attack: list[Puck], extend_attacks_of_length) -> bool: #return True if any attack was extended, False otherwise
    extended_any_attack = False
    print("Extending attacks for puck at " + str(puck.position_on_board) + " with " + str(len(puck.possible_attacks)) + " possible attacks")
    puck_pos_before = copy.deepcopy(puck.position_on_board)
    possible_attacks = [attack for attack in puck.possible_attacks if len(attack) == extend_attacks_of_length] #we will modify the list, so we need a copy
    for attack in possible_attacks:
        if extend_attack(attack, puck, allies_before_any_attack, enemies_before_any_attack):
            extended_any_attack = True
    puck.move_to(puck_pos_before)
    print("After extending attacks, puck at " + str(puck.position_on_board) + " has " + str(len(puck.possible_attacks)) + " possible attacks")
    return extended_any_attack

def count_puck_possible_single_attacks_from_current_tile(puck: Puck, allies: list[Puck], enemies: list[Puck]):
    is_dame = puck.is_dame
    for direction in State.directions:
        if is_dame:
            if fill_puck_attack_in_direction(puck, direction[0], direction[1], allies, enemies):
                return True
        else:
            if fill_puck_attack_tile(puck, direction[0], direction[1], allies, enemies):
                return True

def fill_puck_attack_in_direction(puck: Puck, x_change: int, y_change: int, allies: list[Puck], enemies: list[Puck], current_attack: list[tuple[int,int]] = None) -> bool: #return True if attack is possible, False otherwise
    for i in range(1,8): #<1;8), the most tiles a puck can move is 7
        if fill_puck_attack_tile(puck, x_change * i, y_change * i, allies, enemies, current_attack):
            return True
    return False

def fill_puck_attack_tile(puck: Puck, x_change: int, y_change: int, allies: list[Puck], enemies: list[Puck], current_attack: list[tuple[int,int]] = None) -> bool: #return True if attack is possible, False otherwise
    attack_self: bool = x_change == 0 and y_change == 0
    if attack_self:
        print("Invalid tile for attack")
        #TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False
    single_axis_move: bool = abs(x_change) == 0 or abs(y_change) == 0
    if single_axis_move:
        print("Invalid tile for attack")
        # TODO: show message that this is invalid tile for attack
        traceback.print_stack()
        return False

    if puck.is_dame:
        diagonal_move: bool = abs(x_change) == abs(y_change)
        if not diagonal_move:
            print("Invalid tile for attack")
            #TODO: show message that this is invalid tile for attack
            traceback.print_stack()
            return False
    else:
        long_move: bool = abs(x_change) > 1 or abs(y_change) > 1
        if long_move:
            print("Invalid tile for attack")
            #TODO: show message that this is invalid tile for attack
            traceback.print_stack()
            return False

    puck_pos = puck.position_on_board
    tile_pos = (puck_pos[0] + x_change, puck_pos[1] + y_change)
    next_tile_pos = (tile_pos[0] + x_change, tile_pos[1] + y_change)
    if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[1] < 0 or tile_pos[1] > 7:
        #out of bounds, attack not possible, not an exception, expected when checking directions
        return False
    if next_tile_pos[0] < 0 or next_tile_pos[0] > 7 or next_tile_pos[1] < 0 or next_tile_pos[1] > 7:
        #out of bounds, attack not possible, not an exception, expected when checking directions
        return False

    #find enemy on the tile
    if not any(e.position_on_board == tile_pos for e in enemies):
        return False

    #enemy found, check if next tile is empty
    if not BoardOperations.is_tile_empty(next_tile_pos, allies + enemies):
        return False

    #we got here, so the attack is possible
    #add this tile to the attack list
    if current_attack is not None:
        extended_attack = current_attack.copy()
        extended_attack.append(tile_pos)
        puck.possible_attacks.append(extended_attack)
    else:
        puck.possible_attacks.append([tile_pos])
    return True

def extend_attack(attack: list[tuple[int, int]], puck: Puck, allies_before_any_attack: list[Puck], enemies_before_any_attack: list[Puck]) -> bool: #return True if attack was extended, False otherwise
    extended = False
    enemies = copy.deepcopy(enemies_before_any_attack)
    allies = [ally for ally in allies_before_any_attack if not ally.is_same_puck(puck)]
    execute_attack(attack, puck, enemies)
    for direction in State.directions:
        if puck.is_dame:
            if fill_puck_attack_in_direction(puck, direction[0], direction[1], allies, enemies, attack):
                extended = True
        else:
            if fill_puck_attack_tile(puck, direction[0], direction[1], allies, enemies, attack):
                extended = True
    return extended
    pass

def execute_attack(attack: list[tuple[int,int]], puck: Puck, enemies: list[Puck]):
    for e in enemies:
        for tile in attack:
            if e.pos == tile:
                enemies.remove(e)
    [BoardOperations.move_puck_after_attack(puck, tile) for tile in attack]
    pass