import pygame
import Init
import GameLoop
import PythonUtils
import State

Init.setup_screen()
Init.setup_clock()
Init.init_state()

while not State.close_requested:
    input_events = pygame.event.get()
    for event in input_events:
        if event.type == pygame.QUIT:
            State.close_requested = True
    GameLoop.execute_loop(input_events)

