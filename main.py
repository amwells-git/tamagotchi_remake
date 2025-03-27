# get common imports
import pygame

from src.common_imports import *

# import save data function
from src.save_game import save_game, load_game
# import image loading functions
from src import image_load
# import event functions
from src import event_handlers as events
# import display functions
from src import display_functions as dis_func

# define initial game data
game_data = gc.GAME_INIT_DATA

# update game data with saved data (if exists)
if not os.path.exists(gc.SAVE_FILE):
    save_game(game_data) # create save file
else:
    game_data = load_game() # load save file

# time since program start
game_data['start_time'] = time.monotonic()

# display variable to be changed by meter btn
# 0 is initial load / tamagotchi view
# 1 is show happy
# 2 is show hunger
# 3 is show discipline
# 4 is show age
# 5 is show weight
current_display = 0

# function to update elapsed time / active life span of tamagotchi
def update_elapsed_time():
    global game_data

    current_time = round(time.monotonic())
    game_data['elapsed_time'] += round(current_time - game_data['start_time'])
    game_data['start_time'] = current_time
    
# pygame setup
pygame.init()
# initialize display
display = pygame.display.set_mode((gc.WIDTH, gc.HEIGHT))
pygame.display.set_caption('~Tamagotchi Recreated~')
# game loop variables
clock = pygame.time.Clock()
run = True
# game images
btn_images = image_load.get_btn_images()
stage_images = image_load.get_stage_images(game_data['teen_ver'], game_data['adult_ver'])
stat_images = image_load.get_stat_images()
condition_images = image_load.get_condition_images()
# font
GAME_FONT = pygame.font.SysFont(gc.FONT_STYLE, gc.FONT_SIZE)

# define btn locations
btn_locations = {
    # top row
    "food": btn_images["food"].get_rect(topleft=gc.BTN_ROW_TOP),
    "light_off": btn_images["light_off"].get_rect(topleft=(2 * gc.BTN_ROW_TOP[0] - gc.BTN_GAP, gc.BTN_ROW_TOP[1])),
    "light_on": btn_images["light_on"].get_rect(topleft=(2 * gc.BTN_ROW_TOP[0] - gc.BTN_GAP, gc.BTN_ROW_TOP[1] + gc.BTN_SIZE + 10)),
    "game": btn_images["game"].get_rect(topleft=(3 * gc.BTN_ROW_TOP[0] - gc.BTN_GAP, gc.BTN_ROW_TOP[1])),
    "medicine": btn_images["medicine"].get_rect(topleft=(4 * gc.BTN_ROW_TOP[0] - gc.BTN_GAP, gc.BTN_ROW_TOP[1])),
    # bottom row
    "bathroom": btn_images["bathroom"].get_rect(topleft=gc.BTN_ROW_BOTTOM),
    "meter": btn_images["meter"].get_rect(topleft=(2 * gc.BTN_ROW_BOTTOM[0] - gc.BTN_GAP, gc.BTN_ROW_BOTTOM[1])),
    "discipline": btn_images["discipline"].get_rect(topleft=(3 * gc.BTN_ROW_BOTTOM[0] - gc.BTN_GAP, gc.BTN_ROW_BOTTOM[1])),
    "attention_wanted": btn_images["attention_wanted"].get_rect(topleft=(4 * gc.BTN_ROW_BOTTOM[0] - gc.BTN_GAP, gc.BTN_ROW_BOTTOM[1])),
    "attention_not_wanted": btn_images["attention_not_wanted"].get_rect(topleft=(4 * gc.BTN_ROW_BOTTOM[0] - gc.BTN_GAP, gc.BTN_ROW_BOTTOM[1])),
}

# define which btns are active
active_btns = {"food", "light_off", "game", "medicine", "bathroom", "meter", "discipline", "attention_not_wanted"}
if not game_data['light']:
    active_btns.clear()
    active_btns.add("light_on")
elif game_data['current_wants']:
    active_btns.remove("attention_not_wanted")
    active_btns.add("attention_wanted")

# game loop
while run:
    clock.tick(gc.FPS)

    # update elapsed time
    update_elapsed_time()

    # call game time event handler
    game_data, active_btns = events.timed_event_handler(game_data, active_btns)

    # call user event handler
    run, game_data, active_btns, current_display = events.pygame_event_handler(game_data, active_btns,
                                                                               current_display, btn_locations)

    # call renderers
    dis_func.fill_display(display, game_data['light']) # fill screen
    dis_func.display_btns(display, active_btns, btn_images, btn_locations) # display active buttons
    dis_func.display_tama(display, game_data, current_display, stage_images, stat_images, GAME_FONT) # display tama / stats
    dis_func.display_sick(display, game_data, condition_images, btn_locations['medicine'].topleft)

    # update game display
    pygame.display.update()

# close program
pygame.quit()