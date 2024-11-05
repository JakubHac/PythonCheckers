import State
from Puck import Puck
from GameState import GameState
import PuckGhostHandler
import PuckAttackHandler

def start():
    State.chosen_puck = None
    State.game_state = GameState.WhiteChooseOwnPuck
    State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
    State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)

def try_select_puck_for_move(puck: Puck):
    if ((State.game_state == GameState.WhiteChooseOwnPuck and puck.is_black())
        or (State.game_state == GameState.BlackChooseOwnPuck and puck.is_white())):
        return
    sorted_allies = State.white_pucks_sorted_by_possible_attacks if puck.is_white() else State.black_pucks_sorted_by_possible_attacks
    if not PuckAttackHandler.this_puck_has_longest_attack(puck, sorted_allies):
        # TODO: show message that this puck cannot attack
        print("This puck cannot attack")
        return
    State.chosen_puck = puck
    PuckGhostHandler.despawn_puck_ghosts()
    print("Puck has " + str(len(puck.possible_attacks)) + " possible attacks")
    if len(puck.possible_attacks) > 0:
        State.game_state = GameState.WhiteChooseAttack if puck.is_white() else GameState.BlackChooseAttack
        PuckGhostHandler.spawn_attack_ghosts()
    else:
        State.game_state = GameState.WhiteChooseMove if puck.is_white() else GameState.BlackChooseMove
        if puck.is_dame:
            PuckGhostHandler.spawn_move_ghosts_for_dame()
        else:
            PuckGhostHandler.spawn_move_ghosts_for_puck()

def puck_clicked(puck: Puck):
    #handle choosing pucks for move
    print("Current state: " + str(State.game_state))
    if State.game_state == GameState.WhiteChooseOwnPuck or State.game_state == GameState.BlackChooseOwnPuck:
        try_select_puck_for_move(puck)
        print("Updated state: " + str(State.game_state))
    #handle puck movement
    elif State.game_state == GameState.WhiteChooseMove or State.game_state == GameState.BlackChooseMove:
        if puck != State.chosen_puck:
            if puck.color == State.chosen_puck.color:
                try_select_puck_for_move(puck)
                print("Updated state: " + str(State.game_state))
            return
        PuckGhostHandler.despawn_puck_ghosts()
        State.game_state = GameState.WhiteChooseOwnPuck if State.chosen_puck.is_white() else GameState.BlackChooseOwnPuck
        State.chosen_puck = None
        print("Updated state: " + str(State.game_state))
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
