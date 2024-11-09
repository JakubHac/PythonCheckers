import BoardOperations
import State
from GameState import GameState
from PuckGhost import PuckGhost
import PuckAttackHandler

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
    puck = State.chosen_puck
    tiles = set()
    for attack in [atk for atk in puck.possible_attacks if len(atk) > len(State.current_attack_sequence)]:
        attack_start = attack[:len(State.current_attack_sequence)]
        if attack_start == State.current_attack_sequence:
            tiles.add(attack[len(State.current_attack_sequence)])

    for tile in tiles:
        PuckGhost(BoardOperations.get_puck_position_after_attack(puck, tile), State.puck_size, puck.color, attack_puck_ghost_clicked, tile)

def move_puck_ghost_clicked(puck_ghost: PuckGhost):
    if State.game_state == GameState.WhiteChooseMove:
        State.game_state = GameState.BlackChooseOwnPuck
    elif State.game_state == GameState.BlackChooseMove:
        State.game_state = GameState.WhiteChooseOwnPuck

    puck_ghost_position = puck_ghost.position_on_board
    BoardOperations.move_puck(State.chosen_puck, puck_ghost_position)

    if State.chosen_puck.is_black:
        State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks,State.black_player.pucks)
    else:
        State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks,State.white_player.pucks)

    State.chosen_puck = None
    despawn_puck_ghosts()

def attack_puck_ghost_clicked(puck_ghost: PuckGhost):
    BoardOperations.move_puck(State.chosen_puck, puck_ghost.position_on_board)
    State.current_attack_sequence.append(puck_ghost.attack_pos)
    #not working 100% correct, attacking in sequence isn't working properly
    State.chosen_puck.possible_attacks = [attack for attack in State.chosen_puck.possible_attacks if attack[:len(State.current_attack_sequence)] == State.current_attack_sequence and not attack == State.current_attack_sequence]
    despawn_puck_ghosts()
    print("Attack ghost clicked, current game state: " + str(State.game_state))
    if State.game_state == GameState.WhiteChooseAttack:
        player_who_lost_puck = State.black_player
    else:
        player_who_lost_puck = State.white_player

    killed_puck = [puck for puck in player_who_lost_puck.pucks if puck.position_on_board == puck_ghost.attack_pos][0]
    player_who_lost_puck.pucks.remove(killed_puck)
    killed_puck.destroy()

    if len(State.chosen_puck.possible_attacks) == 0:
        State.current_attack_sequence = []
        if len(player_who_lost_puck.pucks) == 0:
            print("Player " + ("white" if player_who_lost_puck.is_white else "black") + " lost")
            State.game_state = GameState.WhiteWon if not player_who_lost_puck.is_white else GameState.BlackWon
        else:
            State.game_state = GameState.WhiteChooseOwnPuck if State.chosen_puck.is_black() else GameState.BlackChooseOwnPuck
            if State.chosen_puck.is_black:
                State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(
                    State.white_player.pucks, State.black_player.pucks)
            else:
                State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(
                    State.black_player.pucks, State.white_player.pucks)
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