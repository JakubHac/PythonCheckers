import pygame
from Square import Square
import State
from MainMenuScreen import MainMenuScreen
import Singletons

def setup_screen():
    pygame.init()
    State.screen = pygame.display.set_mode((State.screen_width, State.screen_height))
    pygame.display.set_caption("Warcaby")

def init_state():
    main_menu_screen = MainMenuScreen()
    State.active_screens.append(Singletons.MainMenuScreen)
    # square1 = Square((40,40), (25,25), (0, 125, 255))
    # square2 = Square((120,40), (25,25), (0, 125, 255))
    # square3 = Square((240,40), (25,25), (125, 125, 255))
    # square4 = Square((360,40), (25,25), (125, 0, 255))
    # main_menu_screen.add_clickable(square1)
    # main_menu_screen.add_clickable(square2)
    # main_menu_screen.add_clickable(square3)
    # main_menu_screen.add_clickable(square4)
    # main_menu_screen.add_tickable(square1)
    # main_menu_screen.add_tickable(square2)
    # main_menu_screen.add_tickable(square3)
    # main_menu_screen.add_tickable(square4)


def setup_clock():
    State.clock = pygame.time.Clock()
    State.clock.tick(60)
    State.delta_time = State.clock.get_time()