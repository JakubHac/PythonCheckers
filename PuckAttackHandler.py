import copy
import traceback
import BoardOperations
import MathUtil
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
    if any([attack for attack in puck.possible_attacks if len(attack) > len(enemies_before_any_attack)]):
        print("Puck at " + str(puck.position_on_board) + " has more possible attacks (" + str(len(puck.possible_attacks)) +") than enemies " + str(len(enemies_before_any_attack)) + ", something went wrong")
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
    for direction in State.directions:
        if is_dame:
            if fill_dame_attack_in_direction(puck, direction[0], direction[1], allies, enemies):
                return True
        else:
            if fill_puck_attack_tile(puck, direction[0], direction[1], allies, enemies):
                return True

def fill_dame_attack_in_direction(puck: Puck, x_change: int, y_change: int, allies: list[Puck], enemies: list[Puck], current_attack: list[tuple[int,int]] = None) -> bool: #return True if attack is possible, False otherwise
    if not puck.is_dame:
        print("This puck is not a dame")
        return False
    for i in range(1,8): #<1;8), the most tiles a puck can move is 7
        is_occupied_by_ally = not BoardOperations.is_tile_empty((puck.position_on_board[0] + x_change * i, puck.position_on_board[1] + y_change * i), allies)
        # if any ally is in the way, we cannot attack in this direction
        if is_occupied_by_ally:
            return False
        # return first to make sure we attack the first enemy in the direction
        if fill_puck_attack_tile(puck, x_change * i, y_change * i, allies, enemies, current_attack):
            return True
    return False

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
    allies = [ally for ally in allies_before_any_attack if not ally.is_same_puck(puck)]
    possible_positions_after_attack = execute_attack(attack, puck, enemies, allies)
    for direction in State.directions:
        if puck.is_dame:
            for possible_positions_after_attack_tile in possible_positions_after_attack:
                puck.move_to(possible_positions_after_attack_tile)
                if fill_dame_attack_in_direction(puck, direction[0], direction[1], allies, enemies, attack):
                    extended = True
        else:
            if fill_puck_attack_tile(puck, direction[0], direction[1], allies, enemies, attack):
                extended = True
    puck.move_to(puck_pos_before)
    return extended
    pass

def execute_attack(attack: list[tuple[int,int]], puck: Puck, enemies: list[Puck], allies: list[Puck]) -> list[tuple[int,int]]: #returns list of tiles where the puck could move after the attack
    removed_enemies = []
    for e in [enemy for enemy in enemies if PythonUtils.list_contains(attack, enemy.position_on_board)]:
        removed_enemies.append(e.position_on_board)
        enemies.remove(e)
    if not puck.is_dame:
        for tile in attack:
            BoardOperations.move_puck_after_attack(puck, tile)
        return [puck.position_on_board]
    else:
        positions_before_attacks = []
        for tile in attack:
            positions_before_attacks.append(puck.position_on_board)
            BoardOperations.move_puck_after_attack(puck, tile)
        position_before_last_attack = positions_before_attacks[-1]
        last_attack = attack[-1]
        direction_of_last_attack = (MathUtil.clamp_np1(last_attack[0] - position_before_last_attack[0]), MathUtil.clamp_np1(last_attack[1] - position_before_last_attack[1]))
        result = []
        for i in range(1,8):
            tile = (last_attack[0] + direction_of_last_attack[0] * i, last_attack[1] + direction_of_last_attack[1] * i)
            if not BoardOperations.is_tile_on_board(tile):
                break
            if not BoardOperations.is_tile_empty(tile, enemies + allies):
                break
            result.append(tile)
        return result