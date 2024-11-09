from GameState import GameState

debug_mouse_clicks = False
show_debug_board = True
is_debug_board = False
screen = None
clock = None
delta_time = 1000/60
screen_color = (15,15,15)
active_screens = []
noto_font_name = "NotoSans-Regular.ttf"
noto_jp_font_name = "NotoSansJP-Regular.ttf"
close_requested = False
screen_width = 1000
screen_height = 1000
tile_size = 100
tile_offset_from_screen = 100
puck_size = 80
game_state = GameState.WhiteChooseOwnPuck
white_player = None
black_player = None
chosen_puck = None
white_pucks_sorted_by_possible_attacks = []
black_pucks_sorted_by_possible_attacks = []
directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ghost_pucks = []
current_attack_sequence = []