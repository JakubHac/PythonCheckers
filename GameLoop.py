import pygame
import State

def execute_loop(input_events):
    State.delta_time = State.clock.get_time()

    for event in input_events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if State.debug_mouse_clicks:
                print(event.__dict__)
            for screen in State.active_screens:
                screen.handle_click(event.pos)

    for screen in State.active_screens:
        screen.tick()

    State.screen.fill(State.screen_color)
    for screen in State.active_screens:
        screen.blit()



    pygame.display.flip()
