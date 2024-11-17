import BoardOperations
import PythonUtils
import State
from GameState import GameState
from PuckGhost import PuckGhost
import PuckAttackHandler
from Puck import Puck

def despawn_puck_ghosts():
    ghosts = State.ghost_pucks.copy()
    for ghost in ghosts:
        ghost.destroy()

def spawn_move_ghosts_for_dame():
    pass

def spawn_move_ghosts_for_puck():
    puck = State.chosen_puck
    for direction in State.directions:
        if puck.is_white() and direction[1] == 1:
            continue
        if puck.is_black() and direction[1] == -1:
            continue
        spawn_ghost_for_tile(puck, direction, move_puck_ghost_clicked)

def spawn_attack_ghosts():
    puck: Puck = State.chosen_puck
    attack_sequence_length = len(State.current_attack_sequence)
    tiles_and_attacks: dict[tuple[int,int], list[list[tuple[int,int]]]] = {}
    for attack in [atk for atk in puck.possible_attacks if len(atk) > attack_sequence_length]:
        attack_start = attack[:attack_sequence_length]
        if attack_start == State.current_attack_sequence:
            tile = attack[attack_sequence_length]
            if tiles_and_attacks.get(tile) is not None:
                tiles_and_attacks[tile].append(attack)
            else:
                tiles_and_attacks[tile] = [attack]

    if not puck.is_dame:
        for tile in tiles_and_attacks.keys():
            PuckGhost(BoardOperations.get_puck_position_after_attack(puck, tile), State.puck_size, puck.color, attack_puck_ghost_clicked, tile)
        return

    tiles_with_ghosts = set()

    for tile in tiles_and_attacks.keys():
        attacks = tiles_and_attacks[tile]
        for attack in attacks:
            is_last_move_in_attack = len(attack) == attack_sequence_length + 1
            direction = tile[0] - puck.position_on_board[0], tile[1] - puck.position_on_board[1]
            if is_last_move_in_attack: #pick any position in the direction of the attack:
                for i in range(1, 8):
                    new_tile = tile[0] + i * direction[0], tile[1] + i * direction[1]
                    if not BoardOperations.is_tile_on_board(new_tile):
                        break
                    if not BoardOperations.is_tile_empty(new_tile, State.white_player.pucks + State.black_player.pucks):
                        break
                    if new_tile not in tiles_with_ghosts:
                        PuckGhost(new_tile, State.puck_size, puck.color, attack_puck_ghost_clicked, tile)
                        tiles_with_ghosts.add(new_tile)
                pass
            else: #spawn ghosts that will lead to the next position in attack
                next_attack = attack[attack_sequence_length + 1]
                for i in range(1, 8):
                    new_tile = tile[0] + i * direction[0], tile[1] + i * direction[1]
                    if not BoardOperations.is_tile_to_take(new_tile, State.white_player.pucks + State.black_player.pucks):
                        break
                    x_diff = next_attack[0] - new_tile[0]
                    y_diff = next_attack[1] - new_tile[1]
                    if abs(x_diff) != abs(y_diff):
                        continue
                    if new_tile not in tiles_with_ghosts:
                        PuckGhost(new_tile, State.puck_size, puck.color, attack_puck_ghost_clicked, tile)
                        tiles_with_ghosts.add(new_tile)
                pass

def move_puck_ghost_clicked(puck_ghost: PuckGhost):
    if State.game_state == GameState.WhiteChooseMove:
        State.game_state = GameState.BlackChooseOwnPuck
    elif State.game_state == GameState.BlackChooseMove:
        State.game_state = GameState.WhiteChooseOwnPuck

    State.chosen_puck.move_to(puck_ghost.position_on_board)

    if State.chosen_puck.is_black:
        State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks,State.black_player.pucks)
    else:
        State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks,State.white_player.pucks)

    State.chosen_puck = None
    despawn_puck_ghosts()

def attack_puck_ghost_clicked(puck_ghost: PuckGhost):
    State.chosen_puck.move_to(puck_ghost.position_on_board)
    State.current_attack_sequence.append(puck_ghost.attack_pos)

    State.chosen_puck.possible_attacks = [attack for attack in State.chosen_puck.possible_attacks if PythonUtils.is_a_beginning_of_b(State.current_attack_sequence, attack) and not PythonUtils.is_list_a_equal_to_b(attack, State.current_attack_sequence)]
    if State.game_state == GameState.WhiteChooseAttack:
        player_who_lost_puck = State.black_player
    else:
        player_who_lost_puck = State.white_player

    killed_puck = [puck for puck in player_who_lost_puck.pucks if puck.position_on_board == puck_ghost.attack_pos][0]
    player_who_lost_puck.pucks.remove(killed_puck)
    killed_puck.destroy()
    despawn_puck_ghosts()
    if len(State.chosen_puck.possible_attacks) == 0:
        State.current_attack_sequence = []
        if len(player_who_lost_puck.pucks) == 0:
            print("Player " + ("white" if player_who_lost_puck.is_white else "black") + " lost")
            State.game_state = GameState.WhiteWon if not player_who_lost_puck.is_white else GameState.BlackWon
        else:
            State.game_state = GameState.WhiteChooseOwnPuck if State.chosen_puck.is_black() else GameState.BlackChooseOwnPuck
            if State.chosen_puck.is_black():
                State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
            else:
                State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)
        State.chosen_puck = None
    else:
        spawn_attack_ghosts()

def spawn_ghost_for_tile(puck, direction, on_click: callable):
    tile_pos: tuple[int, int] = (puck.position_on_board[0] + direction[0], puck.position_on_board[1] + direction[1])
    if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[1] < 0 or tile_pos[1] > 7:
        #out of bounds
        return

    if BoardOperations.is_tile_empty(tile_pos, State.white_player.pucks + State.black_player.pucks):
        PuckGhost(tile_pos, State.puck_size, puck.color, on_click)