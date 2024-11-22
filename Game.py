import Singletons
import State
from Puck import Puck
from GameState import GameState
import PuckGhostHandler
import PuckAttackHandler
from State import game_state
from TileState import TileState

popup = lambda: Singletons.GameScreen.popup_handler

def start():
    State.chosen_puck = None
    State.game_state = GameState.WhiteChooseOwnPuck
    State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
    State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)
    popup().popup_current_game_state()

def try_select_puck_for_move(puck: Puck):
    if ((State.game_state == GameState.WhiteChooseOwnPuck and puck.is_black())
        or (State.game_state == GameState.BlackChooseOwnPuck and puck.is_white())):
        return
    sorted_allies = State.white_pucks_sorted_by_possible_attacks if puck.is_white() else State.black_pucks_sorted_by_possible_attacks
    if not PuckAttackHandler.this_puck_has_longest_attack(puck, sorted_allies):
        popup().show_popup("To nie ten pionek może zbić najwięcej pionków przeciwnika")
        return
    State.chosen_puck = puck
    PuckGhostHandler.despawn_puck_ghosts()
    if len(puck.possible_attacks) > 0:
        State.game_state = GameState.WhiteChooseAttack if puck.is_white() else GameState.BlackChooseAttack
        PuckGhostHandler.spawn_attack_ghosts()
    else:
        State.game_state = GameState.WhiteChooseMove if puck.is_white() else GameState.BlackChooseMove
        if puck.is_dame:
            PuckGhostHandler.spawn_move_ghosts_for_dame(False, puck)
        else:
            PuckGhostHandler.spawn_move_ghosts_for_puck(False, puck)

def puck_clicked(puck: Puck):
    if State.is_game_popup_shown:
        return #do not allow any actions when popup is shown
    #handle choosing pucks for move
    if State.game_state == GameState.WhiteChooseOwnPuck or State.game_state == GameState.BlackChooseOwnPuck:
        try_select_puck_for_move(puck)
    #handle puck movement
    elif State.game_state == GameState.WhiteChooseMove or State.game_state == GameState.BlackChooseMove or State.game_state == GameState.WhiteChooseAttack or State.game_state == GameState.BlackChooseAttack:
        if puck != State.chosen_puck:
            if puck.color == State.chosen_puck.color:
                try_select_puck_for_move(puck)
            return
        PuckGhostHandler.despawn_puck_ghosts()

        if game_state == GameState.WhiteChooseMove:
            State.game_state = GameState.WhiteChooseOwnPuck
        elif game_state == GameState.WhiteChooseAttack:
            State.game_state = GameState.WhiteChooseOwnPuck
        elif game_state == GameState.BlackChooseMove:
            State.game_state = GameState.BlackChooseOwnPuck
        elif game_state == GameState.BlackChooseAttack:
            State.game_state = GameState.BlackChooseOwnPuck

        State.game_state = GameState.WhiteChooseOwnPuck if State.chosen_puck.is_white() else GameState.BlackChooseOwnPuck
        State.chosen_puck = None
    pass

def quit_game():
    PuckGhostHandler.despawn_puck_ghosts()
    clear_state_after_game()

def clear_state_after_game():
    players = [State.white_player, State.black_player]
    for player in players:
        player.destroy()
    State.white_player = None
    State.black_player = None
    State.game_state = GameState.WhiteChooseOwnPuck
    State.chosen_puck = None
    State.game_state = GameState.WhiteChooseOwnPuck
    State.white_pucks_sorted_by_possible_attacks = []
    State.black_pucks_sorted_by_possible_attacks = []

def set_tile(board_pos: tuple[int, int], tile_state: TileState):
    if not State.is_debug_board:
        print("Cannot set tile on non-debug board")
        return #only for debug board
    if (board_pos[0] + board_pos[1]) % 2 != 1:
        print("Cannot set tile on white tile")
        return
    white_puck_on_tile = [puck for puck in State.white_player.pucks if puck.position_on_board == board_pos]
    black_puck_on_tile = [puck for puck in State.black_player.pucks if puck.position_on_board == board_pos]
    if tile_state == TileState.Empty:
        if len(white_puck_on_tile) > 0:
            State.white_player.remove_puck(white_puck_on_tile[0])
        elif len(black_puck_on_tile) > 0:
            State.black_player.remove_puck(black_puck_on_tile[0])
    elif tile_state == TileState.White:
        if len(white_puck_on_tile) == 0:
            if len(black_puck_on_tile) > 0:
                State.black_player.remove_puck(black_puck_on_tile[0])
            State.white_player.add_puck(board_pos)
    elif tile_state == TileState.Black:
        if len(black_puck_on_tile) == 0:
            if len(white_puck_on_tile) > 0:
                State.white_player.remove_puck(white_puck_on_tile[0])
            State.black_player.add_puck(board_pos)
    elif tile_state == TileState.UnknownDame:
        if len(white_puck_on_tile) > 0:
            if white_puck_on_tile[0].is_dame:
                print("White puck on tile " + str(board_pos) + " is already a dame")
            else:
                print("White puck on tile " + str(board_pos) + " promoted to dame")
                white_puck_on_tile[0].set_dame()
        elif len(black_puck_on_tile) > 0:
            if black_puck_on_tile[0].is_dame:
                print("Black puck on tile " + str(board_pos) + " is already a dame")
            else:
                print("Black puck on tile " + str(board_pos) + " promoted to dame")
                black_puck_on_tile[0].set_dame()
        else:
            print("No puck to promote to dame on tile " + str(board_pos))

    State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)
    State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
    pass

def swap_turn():
    if State.game_state == GameState.WhiteChooseOwnPuck:
        State.game_state = GameState.BlackChooseOwnPuck
        State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)
        popup().popup_current_game_state()
        return
    if State.game_state == GameState.BlackChooseOwnPuck:
        State.game_state = GameState.WhiteChooseOwnPuck
        State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
        popup().popup_current_game_state()
        return
    print("Cannot swap turn in state " + str(State.game_state))
    pass