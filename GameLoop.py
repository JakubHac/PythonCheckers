import pygame
import Game
import State
from TileState import TileState

def execute_loop(input_events):
    State.delta_time = State.clock.get_time()
    mouse_pos = pygame.mouse.get_pos()
    mouse_board_pos: tuple[int, int] = ((mouse_pos[0] - State.tile_offset_from_screen) // State.tile_size, (mouse_pos[1] - State.tile_offset_from_screen) // State.tile_size)
    for event in input_events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if State.debug_mouse_clicks:
                print(event.__dict__)
            for screen in State.active_screens:
                screen.handle_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            # spawn white puck
            Game.set_tile(mouse_board_pos, TileState.White)
            pass
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            # spawn black puck
            Game.set_tile(mouse_board_pos, TileState.Black)
            pass
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            # kill puck near mouse
            Game.set_tile(mouse_board_pos, TileState.Empty)
            pass
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            Game.swap_turn()
            # swap turn
            pass
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            # promote puck to dame
            Game.set_tile(mouse_board_pos, TileState.UnknownDame)
            pass;
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            # print all pucks possible attacks
            if not State.is_debug_board:
                print("Cannot print pucks attacks on non-debug board")
                return
            pucks_attacks = {}
            for puck in [p for p in State.white_player.pucks if len(p.possible_attacks) > 0]:
                pucks_attacks[puck.position_on_board] = puck.possible_attacks
            for puck in [p for p in State.black_player.pucks if len(p.possible_attacks) > 0]:
                pucks_attacks[puck.position_on_board] = puck.possible_attacks
            print("Pucks possible attacks: " + str(pucks_attacks))

    for screen in State.active_screens:
        screen.tick()

    State.screen.fill(State.screen_color)
    for screen in State.active_screens:
        screen.blit()



    pygame.display.flip()
