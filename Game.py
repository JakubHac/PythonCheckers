import State
import copy
import traceback
from GameState import GameState

class Game:
    def __init__(self):
        pass

    def start(self):
        State.chosen_puck = None
        State.game_state = GameState.WhiteChooseOwnPuck
        white_pucks_sorted = []
        black_pucks_sorted = []
        self.calculate_possible_attacks(State.white_player.pucks, State.black_player.pucks, white_pucks_sorted, black_pucks_sorted)

    def puck_clicked(self, puck):
        #handle choosing pucks for move
        if State.game_state == GameState.WhiteChooseOwnPuck:
            if not puck.is_white:
                pass
            if not self.can_white_puck_be_chosen(puck):
                pass
            State.chosen_puck = puck
            State.game_state = self.can_chosen_white_puck_attack()
        elif State.game_state == GameState.BlackChooseOwnPuck:
            if puck.is_white:
                pass
            State.chosen_puck = puck
            State.game_state = self.can_chosen_black_puck_attack()
        elif State.game_state == GameState.WhiteChooseMove:

            pass
        pass

    def can_chosen_white_puck_attack(self):
        can_attack = False
        #get possible attacks
        #if this puck has possible attacks, return the result
        print("UNIMPLEMENTED")
        if can_attack:
            return GameState.WhiteChooseAttack
        else:
            return GameState.WhiteChooseMove

    def can_chosen_black_puck_attack(self):
        can_attack = False
        print("UNIMPLEMENTED")
        if can_attack:
            return GameState.BlackChooseAttack
        else:
            return GameState.BlackChooseMove

    def calculate_possible_attacks(self, in_white_pucks, in_black_pucks, out_white_pucks, out_black_pucks): #and sort them in descending order
        white_pucks = copy.deepcopy(in_white_pucks)
        black_pucks = copy.deepcopy(in_black_pucks)

        #clear possible attacks
        #for each puck, get first possible attacks
        for puck in white_pucks:
            if self.count_puck_possible_single_attacks_from_current_tile(puck, white_pucks, black_pucks):

            pass

        #try to extend all attacks, until no attack can be extended

        #sort by the longest attack
        pass

    def extend_attack(self, puck, allies, enemies):
        pass

    def count_puck_possible_single_attacks_from_current_tile(self, puck, allies, enemies):
        is_dame = puck.is_dame

        if is_dame:
            self.fill_puck_attack_in_direction(puck, 1, 1, allies, enemies)
            self.fill_puck_attack_in_direction(puck, -1, 1, allies, enemies)
            self.fill_puck_attack_in_direction(puck, 1, -1, allies, enemies)
            self.fill_puck_attack_in_direction(puck, -1, -1, allies, enemies)
        else:
            self.fill_puck_attack_tile(puck, 1, 1, allies, enemies)
            self.fill_puck_attack_tile(puck, -1, 1, allies, enemies)
            self.fill_puck_attack_tile(puck, 1, -1, allies, enemies)
            self.fill_puck_attack_tile(puck, -1, -1, allies, enemies)

    def can_white_puck_be_chosen(self, puck):
        # get possible attacks
        # if first puck in sorted list has 0 attacks, return true
        # else, if we have the same amount of attacks as the first puck, return true
        # else, return false
        pass

    def fill_puck_attack_in_direction(self, puck, x_change, y_change, allies, enemies): #return True if attack is possible, False otherwise
        for i in range(1,8): #<1;8), the most tiles a puck can move is 7
            if self.fill_puck_attack_tile(puck, x_change * i, y_change * i, allies, enemies):
                return True
        return False

    def fill_puck_attack_tile(self, puck, x_change, y_change, allies, enemies): #return True if attack is possible, False otherwise
        if x_change == 0 and y_change == 0:
            print("Invalid tile for attack")
            traceback.print_stack()
            return False

        if not puck.is_dame:
            if x_change > 1 or x_change < -1 or y_change > 1 or y_change < -1:
                print("Invalid tile for attack")
                traceback.print_stack()
                return False
            if abs(x_change) + abs(y_change) > 1:
                print("Invalid tile for attack")
                traceback.print_stack()
                return False
        else:
            if abs(x_change) != abs(y_change) and x_change != 0 and y_change != 0:
                print("Invalid tile for attack")
                traceback.print_stack()
                return

        puck_pos = puck.pos
        tile_pos = (puck_pos[0] + x_change, puck_pos[1] + y_change)
        next_tile_pos = (tile_pos[0] + x_change, tile_pos[1] + y_change)
        if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[1] < 0 or tile_pos[1] > 7:
            #out of bounds, attack not possible, expected when checking directions
            return False
        if next_tile_pos[0] < 0 or next_tile_pos[0] > 7 or next_tile_pos[1] < 0 or next_tile_pos[1] > 7:
            # out of bounds, attack not possible, expected when checking directions
            return False

        #check if there is enemy puck on the tile
        # if no, return False
        #if yes, check if next tile is empty
        #if no, return False
        #if yes, return True, and add this tile to the attack list

        #find enemy on the tile
        found_enemy = False
        for enemy in [e for e in enemies if e.pos == tile_pos]:
            found_enemy = True
            break
        if not found_enemy:
            return False

        #enemy found, check if next tile is empty
        for enemy in [e for e in enemies if e.pos == next_tile_pos]:
            return False
        for ally in [a for a in allies if a.pos == next_tile_pos]:
            return False

        #we got here, so the attack is possible
        #add this tile to the attack list
        puck.possible_attacks.append([tile_pos])

        return True

