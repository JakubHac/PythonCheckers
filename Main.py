import pygame
import Init
import GameLoop
import PythonUtils
import State

Init.setup_screen()
Init.setup_clock()
Init.init_state()

b = [(1, 2), (3, 4)]
a = [(1, 2)]

is_python_a_viable_language_for_anything = a in b
do_i_have_to_do_stupid_things_that_should_just_be_properly_implemented = PythonUtils.is_a_sublist_of_b(a, b)
print(is_python_a_viable_language_for_anything)
print(do_i_have_to_do_stupid_things_that_should_just_be_properly_implemented)

while not State.close_requested:
    input_events = pygame.event.get()
    for event in input_events:
        if event.type == pygame.QUIT:
            State.close_requested = True
    GameLoop.execute_loop(input_events)

