from copy import deepcopy
import random

import BoardOperations
import PuckAttackHandler
import PuckGhostHandler
import PythonUtils
import Singletons
import State
from GameState import GameState
from Player import Player
from Puck import Puck

class Bot(Player):
    def __init__(self, name: str, puck_color: tuple[int, int, int], on_puck_click: callable, allied_puck_weight, enemy_puck_weight, allied_dame_weight, enemy_dame_weight):
        super().__init__(name, puck_color, on_puck_click)
        self.allied_puck_weight = allied_puck_weight
        self.enemy_puck_weight = enemy_puck_weight
        self.allied_dame_weight = allied_dame_weight
        self.enemy_dame_weight = enemy_dame_weight
        self.puck_for_action = None
        self.puck_attack = None
        self.puck_move = None
        pass
    pass

    def bot_choose_puck(self, bot_is_white: bool):
        sorted_pucks: list[Puck] = State.white_pucks_sorted_by_possible_attacks if bot_is_white else State.black_pucks_sorted_by_possible_attacks
        enemies = State.black_player.pucks if bot_is_white else State.white_player.pucks
        if len(sorted_pucks) == 0:
            print("Bot has no pucks to choose from")
            return

        any_puck_can_attack = len(sorted_pucks[0].possible_attacks) > 0

        if any_puck_can_attack:
            #choose attack with best score,
            attack_pucks = [puck for puck in sorted_pucks if PuckAttackHandler.this_puck_has_longest_attack(puck, sorted_pucks)]
            best_value = float('-inf')
            best_attack = None
            best_puck_uid = None
            best_position = None
            for attack_puck in attack_pucks:
                for attack in attack_puck.possible_attacks:
                    allies_copy = deepcopy(attack_pucks)
                    puck = [puck for puck in allies_copy if puck.uid == attack_puck.uid][0]
                    allies_copy = [puck for puck in allies_copy if puck.uid != attack_puck.uid]
                    enemies_copy = deepcopy(enemies)
                    possible_positions = PuckAttackHandler.execute_attack(attack, puck, enemies_copy, allies_copy)
                    was_dame = puck.is_dame
                    for pos in possible_positions:
                        puck.move_to(pos)
                        if BoardOperations.is_puck_position_promoting_to_dame(puck.position_on_board, puck) or was_dame:
                            puck.set_dame()
                        else:
                            puck.unset_dame()
                        value = self.score_board_after_enemy_attack(allies_copy + [puck], enemies_copy)
                        if value > best_value:
                            best_value = value
                            best_attack = attack
                            best_puck_uid = puck.uid
                            best_position = pos
            self.puck_for_action = [puck for puck in sorted_pucks if puck.uid == best_puck_uid][0]
            self.puck_attack = best_attack
            self.puck_move = best_position
        else: #we can only move
            #if we can move to become dame, do it
            non_dame_pucks = [puck for puck in sorted_pucks if not puck.is_dame]
            can_become_dames = [puck for puck in non_dame_pucks if BoardOperations.can_puck_become_dame_with_move(puck, sorted_pucks)]
            if len(can_become_dames) > 0:
                #we don't care much about the best puck to become dame
                #we could check if maybe a puck can become dame then execute some amazing attack,
                #but this way the bot can make a mistake (not optimal move) which is more human-like
                puck_to_become_dame = can_become_dames[random.randint(0, len(can_become_dames) - 1)]
                possible_positions = []
                PuckGhostHandler.spawn_move_ghosts_for_puck(True, puck_to_become_dame, possible_positions)
                self.puck_for_action = puck_to_become_dame
                self.puck_move = possible_positions[random.randint(0, len(possible_positions) - 1)]
                self.puck_attack = None
                return
            #choose move with best score
            moveable_pucks = [puck for puck in sorted_pucks if PuckGhostHandler.check_if_puck_has_possible_actions(puck)]
            best_value = float('-inf')
            best_position = None
            best_puck_uid = None
            for puck in moveable_pucks:
                position_before = puck.position_on_board
                possible_positions = []
                if puck.is_dame:
                    PuckGhostHandler.spawn_move_ghosts_for_dame(True, puck, possible_positions)
                else:
                    PuckGhostHandler.spawn_move_ghosts_for_puck(True, puck, possible_positions)
                for pos in possible_positions:
                    puck.move_to(pos)
                    value = self.score_board_after_enemy_attack(moveable_pucks, enemies)
                    if value > best_value:
                        best_value = value
                        best_position = pos
                        best_puck_uid = puck.uid
                puck.move_to(position_before)
            self.puck_for_action = [puck for puck in sorted_pucks if puck.uid == best_puck_uid][0]
            self.puck_move = best_position
            self.puck_attack = None

        if self.puck_attack is not None:
            for enemy in enemies:
                if PythonUtils.list_contains(self.puck_attack, enemy.position_on_board):
                    enemy.destroy()

            PuckAttackHandler.execute_attack(self.puck_attack, self.puck_for_action, enemies, sorted_pucks)
            self.puck_for_action.move_to(self.puck_move)
            if BoardOperations.is_puck_position_promoting_to_dame(self.puck_for_action.position_on_board, self.puck_for_action):
                self.puck_for_action.set_dame()
        else:
            self.puck_for_action.move_to(self.puck_move)
            if BoardOperations.is_puck_position_promoting_to_dame(self.puck_for_action.position_on_board, self.puck_for_action):
                self.puck_for_action.set_dame()
        pass

    def score_board_after_enemy_attack(self, allies: list[Puck], enemies: list[Puck]):
        enemy_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(enemies, allies)
        can_enemy_attack = len(enemy_pucks_sorted_by_possible_attacks[0].possible_attacks) > 0
        if can_enemy_attack:
            #choose attack with best value
            best_allies = []
            best_enemies = []
            best_value = 0
            for enemy_puck in enemy_pucks_sorted_by_possible_attacks:
                for attack in enemy_puck.possible_attacks:
                    allies_copy = deepcopy(allies)
                    enemies_copy = deepcopy(enemies)
                    puck_copy = [enemy for enemy in enemies_copy if enemy.uid == enemy_puck.uid][0]
                    PuckAttackHandler.execute_attack(attack, puck_copy, allies_copy, enemies_copy)
                    if BoardOperations.is_puck_position_promoting_to_dame(puck_copy.position_on_board, puck_copy):
                        puck_copy.set_dame()
                    value = self.score_board_state(enemies_copy, allies_copy)
                    if value > best_value:
                        best_value = value
                        best_allies = allies_copy
                        best_enemies = enemies_copy

            return self.score_board_state(best_allies, best_enemies)
        else:
            #check if any enemy puck can move to become dame
            #if yes, calculate score as if they have 1 dame more
            #if no, calculate score as is
            non_dane_enemies = [enemy for enemy in enemies if not enemy.is_dame]
            can_become_dames = [enemy for enemy in non_dane_enemies if BoardOperations.can_puck_become_dame_with_move(enemy, enemies + allies)]
            if len(can_become_dames):
                return self.score_board_state(allies, enemies) - self.enemy_dame_weight + self.enemy_puck_weight
            else:
                return self.score_board_state(allies, enemies)
            pass
        pass

    def bot_move_on_popup_close(self, popup):
        bot_is_white = self.is_white
        if State.game_state == GameState.WhiteChooseOwnPuck and bot_is_white:
            self.bot_choose_puck(bot_is_white)

            State.game_state = GameState.BlackChooseOwnPuck

            self.recaluclate_possible_attacks_after_bot_move()

            if not PuckGhostHandler.check_if_current_player_has_any_possible_actions():
                if State.game_state == GameState.WhiteChooseOwnPuck:
                    State.game_state = GameState.BlackWon
                elif State.game_state == GameState.BlackChooseOwnPuck:
                    State.game_state = GameState.WhiteWon

            Singletons.GameScreen.popup_handler.popup_current_game_state()
        elif State.game_state == GameState.BlackChooseOwnPuck and not bot_is_white:
            self.bot_choose_puck(bot_is_white)

            State.game_state = GameState.WhiteChooseOwnPuck

            self.recaluclate_possible_attacks_after_bot_move()

            if not PuckGhostHandler.check_if_current_player_has_any_possible_actions():
                if State.game_state == GameState.WhiteChooseOwnPuck:
                    State.game_state = GameState.BlackWon
                elif State.game_state == GameState.BlackChooseOwnPuck:
                    State.game_state = GameState.WhiteWon

            Singletons.GameScreen.popup_handler.popup_current_game_state()
        pass

    def score_board_state(self, allies, enemies):
        score = 0
        #depending on the weight, bot will be more aggressive or defensive
        for puck in allies:
            score += self.allied_dame_weight if puck.is_dame else self.allied_puck_weight
        for puck in enemies:
            score -= self.enemy_dame_weight if puck.is_dame else self.enemy_puck_weight
        return score

    def recaluclate_possible_attacks_after_bot_move(self):
        if self.is_white:
            State.black_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.black_player.pucks, State.white_player.pucks)
        else:
            State.white_pucks_sorted_by_possible_attacks = PuckAttackHandler.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks)
        pass