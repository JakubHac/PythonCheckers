import copy
import BoardOperations
import PythonUtils
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
    max_attack_length = 1
    while True:
        pucks_with_extended_attacks = []
        for puck in pucks_with_extendable_attacks:
            if extend_attacks(puck, ally_pucks, enemy_pucks, max_attack_length):
                pucks_with_extended_attacks.append(puck)
        if len(pucks_with_extended_attacks) == 0:
            break
        max_attack_length += 1
        pucks_with_extendable_attacks = pucks_with_extended_attacks

    # sort by the longest attack
    ally_pucks_that_can_attack.sort(key=lambda x: max(len(attack) for attack in x.possible_attacks), reverse=True)
    out_ally_pucks = ally_pucks_that_can_attack
    out_ally_pucks += ally_pucks_that_cannot_attack

    # remove attacks that are not the longest, this has to be here or the sorting would not work (max() iterable argument is empty)
    for puck in out_ally_pucks:
        puck.possible_attacks = [attack for attack in puck.possible_attacks if len(attack) == max_attack_length]

    return out_ally_pucks

def this_puck_has_longest_attack(puck: Puck, allies_sorted_by_possible_attacks: list[Puck]) -> bool:
    best_ally = allies_sorted_by_possible_attacks[0]
    max_length_of_allied_attack = 0 if len(best_ally.possible_attacks) == 0 else max(len(attack) for attack in best_ally.possible_attacks)
    max_length_of_our_attack = 0 if len(puck.possible_attacks) == 0 else max(len(attack) for attack in puck.possible_attacks)
    return max_length_of_our_attack == max_length_of_allied_attack

def extend_attacks(puck: Puck, allies_before_any_attack: list[Puck], enemies_before_any_attack: list[Puck], extend_attacks_of_length) -> bool: #return True if any attack was extended, False otherwise
    lengths_of_attacks = [len(attack) for attack in puck.possible_attacks]
    max_length_of_attack = max(lengths_of_attacks) if len(lengths_of_attacks) > 0 else 0
    if any(length for length in lengths_of_attacks if length > len(enemies_before_any_attack)):
        print("Puck at " + str(puck.position_on_board) + " has a longer possible attack (" + str(max_length_of_attack) + ") than enemies " + str(len(enemies_before_any_attack)) + ", something went wrong")
        for attack in puck.possible_attacks:
            print(attack)
        return False
    extended_any_attack = False
    possible_attacks = [attack for attack in puck.possible_attacks if len(attack) == extend_attacks_of_length] #we will modify the list, so we need a copy
    for attack in possible_attacks:
        if extend_attack(attack, puck, allies_before_any_attack, enemies_before_any_attack):
            extended_any_attack = True
    return extended_any_attack

def count_puck_possible_single_attacks_from_current_tile(puck: Puck, allies: list[Puck], enemies: list[Puck]):
    is_dame = puck.is_dame
    can_attack = False
    allies_without_this_puck = [ally for ally in allies if not ally.is_same_puck(puck)]
    for direction in State.directions:
        if is_dame:
            if fill_dame_attack_in_direction(puck, direction[0], direction[1], allies_without_this_puck, enemies):
                can_attack = True
        else:
            if fill_puck_attack_tile(puck, direction[0], direction[1], allies, enemies):
                can_attack = True
    return can_attack

def fill_dame_attack_in_direction(puck: Puck, x_change: int, y_change: int, allies: list[Puck], enemies: list[Puck], current_attack: list[tuple[int,int]] = None) -> bool: #return True if attack is possible, False otherwise
    if not puck.is_dame:
        print("This puck is not a dame")
        return False
    can_attack = False
    for i in range(1,8): #<1;8), the most tiles a puck can move is 7
        previous_tile = (puck.position_on_board[0] + x_change * (i - 1), puck.position_on_board[1] + y_change * (i - 1))
        if not BoardOperations.is_tile_to_take(previous_tile, enemies + allies):
            return can_attack
        if fill_puck_attack_tile(puck, x_change * i, y_change * i, allies, enemies, current_attack):
            can_attack = True
    return can_attack

def fill_puck_attack_tile(puck: Puck, x_change: int, y_change: int, allies: list[Puck], enemies: list[Puck], current_attack: list[tuple[int,int]] = None) -> bool: #return True if attack is possible, False otherwise
    tile_pos = (puck.position_on_board[0] + x_change, puck.position_on_board[1] + y_change)
    if not BoardOperations.is_attack_valid(puck.position_on_board, tile_pos, puck.is_dame, allies, enemies):
        return False
    #we got here, so the attack is possible
    #add this tile to the attack list
    if current_attack is not None:
        extended_attack = current_attack.copy()
        extended_attack.append(tile_pos)
        if not PythonUtils.list_contains(puck.possible_attacks, extended_attack):
            puck.possible_attacks.append(extended_attack)
    else:
        if not PythonUtils.list_contains(puck.possible_attacks, [tile_pos]):
            puck.possible_attacks.append([tile_pos])
    return True

def extend_attack(attack: list[tuple[int, int]], puck: Puck, allies_before_any_attack: list[Puck], enemies_before_any_attack: list[Puck]) -> bool: #return True if attack was extended, False otherwise
    extended = False
    enemies = copy.deepcopy(enemies_before_any_attack)
    puck_pos_before = copy.deepcopy(puck.position_on_board)
    allies_without_this_puck = [ally for ally in allies_before_any_attack if not ally.is_same_puck(puck)]
    possible_positions_after_attack = execute_attack(attack, puck, enemies, allies_without_this_puck)
    for direction in State.directions:
        for possible_positions_after_attack_tile in possible_positions_after_attack:
            puck.move_to(possible_positions_after_attack_tile)
            if puck.is_dame:
                if fill_dame_attack_in_direction(puck, direction[0], direction[1], allies_without_this_puck, enemies, attack):
                    extended = True
            else:
                if fill_puck_attack_tile(puck, direction[0], direction[1], allies_without_this_puck, enemies, attack):
                    extended = True
    puck.move_to(puck_pos_before)
    return extended
    pass

def execute_attack(attack: list[tuple[int,int]], puck: Puck, enemies: list[Puck], allies: list[Puck]) -> list[tuple[int,int]]: #returns list of tiles where the puck could move after the attack
    for e in [enemy for enemy in enemies if PythonUtils.list_contains(attack, enemy.position_on_board)]:
        enemies.remove(e)
    if not puck.is_dame:
        for tile in attack:
            BoardOperations.move_puck_after_attack(puck, tile)
        return [puck.position_on_board]
    else:
        positions_before_attacks = BoardOperations.get_dame_positions_before_attacks(puck, attack)
        position_before_last_attack = positions_before_attacks[-1]
        last_attack = attack[-1]
        puck.move_to(position_before_last_attack)
        direction_of_last_attack = BoardOperations.get_direction_of_attack(position_before_last_attack, last_attack)
        result = []
        for i in range(1,8):
            tile = (last_attack[0] + direction_of_last_attack[0] * i, last_attack[1] + direction_of_last_attack[1] * i)
            if not BoardOperations.is_tile_on_board(tile):
                break
            if not BoardOperations.is_tile_empty(tile, enemies + allies):
                break
            result.append(tile)
        return result